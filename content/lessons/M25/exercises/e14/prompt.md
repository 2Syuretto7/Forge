# Break it: maximum likelihood with tiny samples

Three tails in three flips gives $\hat p = 0$. Measure what that costs on new data.

- `mle_p(k, n)` and `smoothed_p(k, n, alpha)`: the MLE and the posterior mean under a symmetric $\text{Beta}(\alpha, \alpha)$ prior, $(k + \alpha)/(n + 2\alpha)$.
- `heldout_logloss(p, k_test, n_test)`: the average negative log-likelihood per flip of $k_{\text{test}}$ heads in $n_{\text{test}}$ new flips. Return `float("inf")` when a flip that happened was given probability zero.
- `expected_logloss(estimator, p_true, n_train, n_test, trials, seed)`: repeat `trials` times: draw `k ~ Binomial(n_train, p_true)` and `k_test ~ Binomial(n_test, p_true)` from `np.random.default_rng(seed)` (in that order each trial), fit with `estimator(k, n_train)`, and average the held-out log-loss. If any trial is infinite, the average is infinite.

## Hints

1. Treat $0 \cdot \log 0$ as 0: only include a term when its count is positive.
2. `rng.binomial(n, p)` draws one count.
3. With `alpha = 1` (Laplace smoothing) the loss is always finite.
