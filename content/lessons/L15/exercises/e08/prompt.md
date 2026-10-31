# Finding the bad examples

A loss spike often comes from a few corrupted examples in one batch. Their per-example losses stand out, but a mean and standard deviation computed over the batch are dragged up by the outliers themselves.

Implement `outlier_examples(per_example_loss, k=10.0)`: the indices whose loss exceeds the median by more than $k$ **median absolute deviations**.

## Hints

1. MAD is the median of $|x_i - \text{median}(x)|$; both medians ignore a few extreme values.
2. Guard against a MAD of zero with a tiny floor.
3. Log the indices (document ids) of flagged examples, so the data can be inspected and removed upstream.
