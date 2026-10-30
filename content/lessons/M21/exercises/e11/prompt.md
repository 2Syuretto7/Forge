# A reliability diagram

- `reliability(p, y, bins=10)`: for equal-width bins of the predicted probabilities, a list of `(mean_predicted, observed_frequency, count)` for every non-empty bin.
- `ece(p, y, bins=10)`: the expected calibration error, $\sum_b \frac{n_b}{N}\,|\bar p_b - \bar y_b|$.
- `overconfidence(p, y, bins=10)`: the count-weighted average of $\bar p_b - \bar y_b$ over bins with $\bar p_b > \frac12$, positive when the model is too sure of class 1.

The tests compare a calibrated synthetic predictor (ECE near 0) with naive Bayes on the corpus of e10 (provided), whose high-probability bins hold fewer spam messages than it claims.

## Hints

1. Bin index `np.minimum((p * bins).astype(int), bins - 1)`.
2. Skip empty bins.
3. A calibrated predictor: draw $p$ uniformly and $y$ as Bernoulli($p$).
