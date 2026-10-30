# A word never seen

- `fit_alpha(X, y, alpha)`: naive Bayes word probabilities with smoothing `alpha` (return `log_word` of shape `(2, V)`, using `np.log` even when a count is 0, which gives `-inf`).
- `log_odds_alpha(X, y, x, alpha)`: the log-odds of document `x` under that model (equal class priors); `-inf`, `inf` or `nan` are possible without smoothing.
- `veto(X, y, x)`: whether the unsmoothed log-odds is infinite or undefined while the smoothed one (alpha = 1) is finite.

## Hints

1. `np.errstate(divide="ignore", invalid="ignore")` silences the warnings for `log(0)`.
2. With equal priors, the log-odds is `x @ (lw[1] - lw[0])`.
3. `-inf - (-inf)` is `nan`; `0 * -inf` is `nan` as well.
