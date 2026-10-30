# Exact partial sums

Use `fractions.Fraction` so every sum is exact.

- `partial_sums(term, n)`: the list $S_1, \dots, S_n$ where $S_k = \text{term}(1) + \dots + \text{term}(k)$. `term` returns Fractions (or integers).
- `geometric_sum(r, n)`: $1 + r + \dots + r^{n-1}$ for a Fraction `r`, by adding the terms.
- `geometric_closed(r, n)`: the closed form $(r^n - 1)/(r - 1)$, or `n` when $r = 1$.

The tests check an **invariant**: for many random fractions `r` and lengths `n`, the added-up sum and the closed form are exactly equal, as Fractions, with no tolerance at all.

## Hints

1. Keep a running total `s = Fraction(0)` and append it after each term.
2. `r ** k` works for Fractions and stays exact.
3. Exact equality is `==` on Fractions.
