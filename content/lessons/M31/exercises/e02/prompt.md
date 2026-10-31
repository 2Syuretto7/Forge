# Exact tails against the bounds

For the average of $n$ coin flips with probability $p$, compute the exact chance of missing $p$ by at least $\varepsilon$ and set it against the bounds (Section 1).

- `exact_tail(n, p, eps)`: $\sum_k \binom nk p^k(1 - p)^{n - k}$ over the $k$ with $\lvert k/n - p\rvert \ge \varepsilon$, computed through logarithms (`math.lgamma`).
- `chebyshev(n, p, eps)`: $\frac{p(1 - p)}{n\varepsilon^2}$, capped at 1.
- `hoeffding(n, eps)`: $2e^{-2n\varepsilon^2}$, capped at 1.
- `ratio_table(n, p, eps)`: the dict `{"exact", "chebyshev", "hoeffding"}`.

The tests check that both bounds always hold, that Hoeffding beats Chebyshev for large $n$ (exponential against $1/n$), and that Chebyshev wins for small $n$ when $p(1 - p)$ is small.

## Hints

1. $\log\binom nk = \operatorname{lgamma}(n + 1) - \operatorname{lgamma}(k + 1) - \operatorname{lgamma}(n - k + 1)$.
2. Compare $\lvert k/n - p\rvert$ with $\varepsilon$ minus a hair of rounding tolerance.
3. Neither bound knows the exact distribution; each uses less information than the exact sum.
