# Harmonic numbers

- `harmonic(n)`: $H_n = 1 + \frac{1}{2} + \dots + \frac{1}{n}$ as a float.
- `grouping_bound(k)`: the lower bound $1 + k/2$ for $H_{2^k}$ from Section 4.
- `terms_to_exceed(x)`: the smallest $n$ with $H_n > x$.
- `log_estimate(n)`: $\ln n + 0.5772156649$, the asymptotic value.

The tests check the grouping bound for $k$ up to 20, the estimate's accuracy, and how many terms it takes to pass 5 and 10.

## Hints

1. A loop adding `1 / k`.
2. In `terms_to_exceed`, add terms until the total passes `x`, counting as you go.
3. `math.log` is the natural logarithm.
