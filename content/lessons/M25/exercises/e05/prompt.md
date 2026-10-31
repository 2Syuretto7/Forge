# Poisson maximum likelihood and Fisher information

For counts $x_1, \dots, x_n$ from a Poisson($\lambda$) distribution, the log-likelihood is $\ell(\lambda) = \sum_i (x_i\log\lambda - \lambda - \log x_i!)$. Its derivative, the **score**, is zero at the MLE, and its curvature measures how sharply the data pin $\lambda$ down (Section 3).

- `loglik(lam, x)` and `score(lam, x)` $= \sum_i x_i/\lambda - n$.
- `mle(x)`: the zero of the score, $\bar x$.
- `fisher_information(lam, n)`: the expected curvature $\mathbb{E}[-\ell''(\lambda)] = n/\lambda$.
- `standard_error(x)`: $1/\sqrt{I(\hat\lambda)}$, the curvature-based standard error at the MLE.

The tests run a **gradient check** of the score, and simulate 20,000 datasets to confirm that the spread of $\hat\lambda$ matches $1/\sqrt{I(\lambda)}$ and that $\hat\lambda \pm 1.96\,\text{SE}$ covers $\lambda$ about 95 percent of the time.

## Hints

1. `math.lgamma(k + 1)` is $\log k!$; for an array, `np.vectorize(math.lgamma)`, or drop the term, which does not depend on $\lambda$, from the score.
2. $-\ell''(\lambda) = \sum_i x_i/\lambda^2$, whose expectation is $n/\lambda$.
3. If every count is 0, the MLE is 0 and the curvature-based standard error is 0: a warning sign, not an answer.
