# The number e, three ways

- `e_compounding(n)`: $(1 + 1/n)^n$.
- `e_series(terms)`: $\sum_{k=0}^{\text{terms} - 1} 1/k!$, building each $1/k!$ from the previous one (divide by $k$) rather than computing factorials.
- `terms_for_digits(d)`: the smallest number of series terms whose sum is within $10^{-d}$ of `math.e`.
- `compounding_error(n)`: $e - (1 + 1/n)^n$. For large $n$ it is close to $e/(2n)$; the tests check that.

Compare: the series reaches 12 digits with about 15 terms; compounding a million times reaches only 6.

## Hints

1. `(1 + 1 / n) ** n`.
2. Keep `term = 1.0` and `term /= k` at each step after adding it.
3. Increase the number of terms until the error is small enough.
