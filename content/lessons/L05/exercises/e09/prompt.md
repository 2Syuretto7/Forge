# Calibration curves and expected calibration error

For a classifier's predicted probabilities `P` `(n, K)` and labels `y`, use the **confidence** $c_i = \max_k P_{ik}$ and **correctness** $a_i = [\arg\max_k P_{ik} = y_i]$.

- `calibration_bins(P, y, n_bins)`: split $(0, 1]$ into `n_bins` equal-width bins (a confidence of exactly 1 goes in the last bin; bin $b$ holds $c \in (b/n, (b+1)/n]$). Return three arrays of length `n_bins`: mean confidence, accuracy, and count per bin (use 0 for the means of empty bins).
- `ece(P, y, n_bins)`: $\sum_b \frac{n_b}{n}|\text{acc}_b - \text{conf}_b|$ over nonempty bins.

The tests use a synthetic perfectly calibrated predictor (ECE near 0) and an overconfident one.

## Hints

1. `idx = np.minimum(np.ceil(c * n_bins).astype(int) - 1, n_bins - 1)`, then clip below at 0.
2. Loop over bins with a mask.
3. ECE weights each bin by its share of the data.
