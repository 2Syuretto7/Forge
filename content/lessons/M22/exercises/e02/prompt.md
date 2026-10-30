# Probability mass functions

Implement the discrete families of Section 4. Each function returns a float and returns 0 outside the support.

- `bernoulli_pmf(k, p)`: $P(X = k)$ for $k \in \{0, 1\}$.
- `binomial_pmf(k, n, p)`: $\binom{n}{k} p^k (1 - p)^{n - k}$ for $0 \le k \le n$.
- `poisson_pmf(k, lam)`: $e^{-\lambda} \lambda^k / k!$ for $k \ge 0$, computed through logarithms so that $k = 150$ does not overflow.
- `cdf_from_pmf(pmf, k)`: $P(X \le k) = \sum_{j=0}^{k} \text{pmf}(j)$ for a pmf on the nonnegative integers.

The tests check that each pmf sums to 1, has the mean and variance of the table, and that Binomial($n$, $\lambda/n$) approaches Poisson($\lambda$).

## Hints

1. `math.comb(n, k)` is the binomial coefficient.
2. $\log(\lambda^k / k!) = k \log\lambda - \log\Gamma(k + 1)$, and `math.lgamma` is $\log\Gamma$.
3. `pmf` is a function of one integer: `cdf_from_pmf(lambda j: binomial_pmf(j, 3, 0.5), 1)`.
