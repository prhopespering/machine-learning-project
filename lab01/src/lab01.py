"""Lab 1 — Environment Setup & Pandas Data Handling (EDA).

Machine Learning Project (53744-01), Fall 2026.

Fill in every TODO block. Do NOT rename functions or change their
signatures/return types — automated (public + hidden) tests call them directly.
Run:      python src/lab01.py
Self-check: python -m pytest tests/ -q
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

# ---- Fill in your information (used in results.json) ----
STUDENT_ID = "50261637"             # TODO: your student id, e.g. "20261234"
STUDENT_NAME = "MouhamedDouina"     # TODO: your name in Korean or roman letters — "홍길동" / "HongGildong"

SEED = 42  # fixed for the whole course — DO NOT CHANGE
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "cafe_sales.csv"


def set_seed(seed: int = SEED) -> None:
    """DO NOT MODIFY."""
    np.random.seed(seed)


def load_data(path: str | Path) -> pd.DataFrame:
    """DO NOT MODIFY. Loads the raw csv exactly as stored."""
    return pd.read_csv(path)


# ======================= TODO (Task 1): missing values =======================
def summarize_missing(df: pd.DataFrame) -> pd.Series:
    """Return the number of missing (NaN) values per column.

    Returns:
        pd.Series indexed by column name, integer counts, sorted in
        DESCENDING order of count (ties: keep pandas' stable order).
        Include only columns that have at least one missing value.
    """
    mask = df.isna()
    missing = mask.sum()
    missing = missing[missing > 0]
    # keep original order in case of equal value of `missing`
    missing = missing.sort_values(ascending = False, kind = "stable")
    return missing
# ============================ END TODO (Task 1) ==============================


# ======================== TODO (Task 2): cleaning ============================
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned COPY of df (do not mutate the input). Steps, in order:

    1. Drop exact duplicate rows (keep the first occurrence), reset the index.
    2. Convert `unit_price` to float. Some values are strings with a
       thousands separator, e.g. "4,500" -> 4500.0.
    3. Fill missing `quantity` with the MEDIAN of the non-missing quantities
       (computed AFTER step 1), then cast `quantity` to int.
    4. Recompute `total_price` = unit_price * quantity for rows where
       `total_price` is missing; leave existing values untouched.
    5. Fill missing `customer_rating` with the column MEAN (computed after
       step 1) rounded to 2 decimals — i.e. the FILL VALUE is `round(mean, 2)`;
       do not round the existing ratings or the whole column.

    The returned frame must contain no missing values.
    """
    # create a copy of the provided dataframe using df.copy
    clean = df.copy()
    # clear out duplicates in the copy
    clean = clean.drop_duplicates(keep = "first").reset_index(drop = True)
    # transform string based price with .str.replace into float value using .astype
    clean["unit_price"] = pd.to_numeric(clean["unit_price"].astype(str).str.replace(",", "", regex = False).astype(float))
    # using .median to find median value of non missing values
    median_quantity = clean["quantity"].median()
    # here we fill the missing quantity with the median of non missing quantities
    # using `fillna` func
    # we aswell turn this value into int type
    clean["quantity"] = (clean["quantity"].fillna(median_quantity).astype(int))
    # simple missing total price value computing
    clean["total_price"] = clean["total_price"].fillna(clean["unit_price"] * clean["quantity"])
    # we calculate the rating mean in order to replace the NaN values
    # with rating_mean
    rating_mean = round(clean["customer_rating"].mean(), 2)
    clean["customer_rating"] = clean["customer_rating"].fillna(rating_mean)
    return clean
# ============================ END TODO (Task 2) ==============================


# ======================= TODO (Task 3): outliers (IQR) =======================
def detect_outliers_iqr(df: pd.DataFrame, column: str, k: float = 1.5) -> list:
    """Return the sorted list of index labels whose `column` value is an
    outlier under the IQR rule:

        value < Q1 - k*IQR   or   value > Q3 + k*IQR,
        where IQR = Q3 - Q1 (Q1/Q3 = 25th/75th percentiles, pandas default).

    NaN values are never outliers. Return a plain Python list of ints.
    """
    values = df[column]
    value_q1 = values.quantile(0.25)
    value_q3 = values.quantile(0.75)
    iqr = value_q3 - value_q1
    # defining limits where value in betweens is not anormal
    lower_bound = value_q1 - k * iqr
    upper_bound = value_q3 + k * iqr
    # identify outliers with iqr bounds
    mask = (values < lower_bound) | (values > upper_bound)
    return sorted(df.index[mask].tolist())
# ============================ END TODO (Task 3) ==============================


# ====================== TODO (Task 4): group statistics ======================
def compute_group_stats(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Group df by `group_col` and aggregate `value_col`.

    Returns:
        DataFrame indexed by the group keys with exactly three columns
        ["count", "mean", "sum"] (count of non-missing values, mean rounded
        to 2 decimals, sum), sorted by "sum" in DESCENDING order.
    """
    stats = df.groupby(group_col)[value_col].agg(["count", "mean", "sum"])
    stats["mean"] = stats["mean"].round(2)
    return stats.sort_values("sum", ascending = False, kind = "stable")
# ============================ END TODO (Task 4) ==============================


def main() -> dict:
    """DO NOT MODIFY (except nothing — really, do not modify).

    Runs the full EDA pipeline and writes results.json next to the repo root.
    """
    set_seed()
    t0 = time.time()
    raw = load_data(DATA_PATH)
    missing = summarize_missing(raw)
    clean = clean_data(raw)
    outliers = detect_outliers_iqr(clean, "quantity")
    stats = compute_group_stats(clean, "category", "total_price")
    results = {
        "lab": "lab01",
        "student_id": STUDENT_ID,
        "name": STUDENT_NAME,
        "seed": SEED,
        "metrics": {
            "n_rows_raw": int(len(raw)),
            "n_rows_clean": int(len(clean)),
            "n_duplicates_removed": int(len(raw) - len(clean)),
            "missing_total_raw": int(missing.sum()),
            "missing_total_clean": int(clean.isna().sum().sum()),
            "n_outliers_quantity": int(len(outliers)),
            "top_category_by_revenue": str(stats.index[0]),
            "mean_rating_clean": float(round(clean["customer_rating"].mean(), 3)),
        },
        "runtime_seconds": round(time.time() - t0, 2),
    }
    out = Path(__file__).resolve().parent.parent / "results.json"
    out.write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
