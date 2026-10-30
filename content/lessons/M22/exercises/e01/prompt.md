# Expectation and variance of a discrete distribution

Implement the moments of Sections 2 and 3 for a discrete random variable given by its `values` and `probs` (1-D arrays of equal length; `probs` sums to 1).

- `moments(values, probs)` returns `(mean, variance)` as floats, with variance computed as $\mathbb{E}[(X - \mathbb{E}X)^2]$.
- `affine_moments(mean, var, a, b)` returns the mean and variance of $aX + b$.
- `average_variance(var, n)` returns the variance of the mean of `n` independent copies.

## Hints

1. `mean = np.sum(values * probs)`.
2. Variance scales by $a^2$ and ignores the shift $b$.
3. Independent variances add, and dividing by $n$ divides the variance by $n^2$.
