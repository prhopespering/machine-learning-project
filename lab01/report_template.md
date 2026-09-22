# Lab 1 Report - 50261637 MouhamedDouina

## 1. What I did

I removed exact duplicate rows before computing the median used for `quantity` imputation, so repeated records would not influence the replacement value. I treated missing fields according to their meaning: `quantity` was filled with the median, `customer_rating` with the rounded mean, and `total_price` was recomputed from `unit_price * quantity` instead of using a general statistic. I kept the three IQR-flagged quantities because they are plausible bulk orders rather than clear data-entry errors, and interpreted them as a source of skew in the revenue distribution.

## 2. Results

**Table 1. Key numbers from `results.json`.** The three quantity outliers are especially
important because they help explain why the `total_price` distribution is strongly right-skewed
and why summary statistics such as the mean can be influenced by unusually large orders.

| Metric | Value |
|--------|-------|
| Rows raw / clean | 412 / 400 |
| Duplicates removed | 12 |
| Missing values (raw → clean) | 103 → 0 |
| Quantity outliers (IQR) | 3 |
| Top category by revenue | coffee |
| Mean rating (clean) | 4.037 |

## 3. Figures

![Figure 1 — Missing values per column](notebooks/fig1.png)

**Figure 1. Missing values per column.**
The missing ratings are not surprising because giving feedback is optional, and many customers may not want to spend time rating a business or may not rate it again on a later visit. However, the missing `quantity` and `total_price` values suggest weaknesses in the order-recording process because they affect the ability to reconstruct revenue. Imputation can make the table complete, but it cannot recover the information that was never recorded, so the data-collection system should be improved.

![Figure 2 — Distribution of total price](notebooks/fig2.png)

**Figure 2. Distribution of `total_price` after cleaning.** The distribution is strongly right-skewed
because a few bulk orders have much higher totals than ordinary orders. The median would therefore
be a more robust single summary than the mean. Moreover the IQR rule could be used to separate
ordinary and bulk orders and report the mean for each group.

![Figure 3 — Customer rating by category](notebooks/fig3.png)

**Figure 3. `customer_rating` by category after cleaning.** Tea has the highest mean rating
(4.206), but it is based on only 66 ratings, compared with 178 for coffee. The difference is
interesting, but less reliable than a difference observed in a much larger group.

## 4. Interpretation

The cleaning process removed 12 exact duplicate rows, reducing the dataset from 412 to 400
observations (Table 1). Removing these duplicates before computing the median and mean prevents
repeated transactions from receiving extra weight. The missing values were handled differently
according to their meaning: `quantity` was imputed with the post-deduplication median,
`customer_rating` with the rounded mean, and missing `total_price` values were derived from
`unit_price * quantity`; this makes the cleaned table complete, but it does not recover the
information that was absent from the original collection (Figure 1)!

The IQR rule flagged three unusually large quantities: 120, 150, and 200 units. These values are
plausible bulk orders rather than obvious data-entry errors, so removing them would not be
justified without additional business information. They explain the long right tail in the
`total_price` histogram (Figure 2) and can pull the mean upward, which is why the median or
separate summaries for ordinary and bulk orders may be more informative. Finally, `coffee` remains
the top category by total revenue, but its lead is partly explained by its larger group size (178
rows versus 81 for `dessert`); its total revenue should therefore not be interpreted as the
highest revenue per order (Table 1). The higher mean rating for `tea` should also be interpreted
cautiously because it is based on only 66 ratings (Figure 3).

## 5. Limitations

The main limitation is the data-collection design rather than the cleaning code. A revised system
should validate required transactional fields at entry time, preserve bulk orders in a separate
flagged workflow or table, and store customer ratings in a separate feedback dataset linked to the
order or customer. Mixing optional customer feedback with transactional variables such as quantity
and revenue makes it harder to distinguish a missing opinion from a defective sales record, and a
schema review could therefore change both the imputation strategy and the conclusions about order
statistics.

## AI & external-code usage

| Tool / Source | Part used for | What I modified & verified myself |
|---------------|---------------|-----------------------------------|
| OpenAI Codex (GPT-5.6 Luna; reasoning effort: High), following the repository rules in [`AGENT.md`](../AGENT.md) | Step-by-step reasoning about pandas cleaning, missing-value handling, duplicate removal, IQR outlier detection, grouped statistics, plotting, debugging public-test failures, and Lab 1 report interpretation | I wrote and edited the implementation and report, adapted the guidance to the Lab 1 specifications, understood each submitted line, ran the public tests, executed the notebook, and verified the generated figures and `results.json`. |
| [GeeksforGeeks](https://www.geeksforgeeks.org) | Python and pandas function syntax lookup | I adapted the syntax to this lab, checked its behavior against the function specifications and public tests, and verified the final results myself. |
