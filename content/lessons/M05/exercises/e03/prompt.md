# Sigma notation

- `sigma(f, lo, hi)`: $\sum_{k=\text{lo}}^{\text{hi}} f(k)$, including both ends; an empty sum (`hi < lo`) is 0.
- `shift_index(f, lo, hi, s)`: the same sum written with the index shifted by `s`: $\sum_{j = \text{lo} + s}^{\text{hi} + s} f(j - s)$. It must equal `sigma(f, lo, hi)`.
- `split(f, lo, mid, hi)`: the pair of sums from `lo` to `mid` and from `mid + 1` to `hi`, whose total is the whole sum.

The tests check an **invariant**: linearity. For random coefficients `a`, `b` and random functions, $\sum (a f(k) + b g(k)) = a \sum f(k) + b \sum g(k)$.

## Hints

1. `sum(f(k) for k in range(lo, hi + 1))`.
2. Shifting is renaming: `sigma(lambda j: f(j - s), lo + s, hi + s)`.
3. Linearity is exactly what makes every closed form in this lesson possible.
