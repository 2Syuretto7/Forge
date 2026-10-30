# Factor once, solve many

Count operations exactly (a multiply, add, subtract or divide each counts 1).

- `lu_flops(n)`: elimination without the right-hand side. At step $k$ (from 1 to $n - 1$), with $j = n - k$ rows left below the pivot: $j$ divisions for the multipliers and $j^2$ multiply-subtract pairs, so $j + 2j^2$ operations.
- `tri_flops(n)`: one triangular solve of size $n$: $n^2$.
- `many_rhs_flops(n, k, refactor)`: the total for $k$ right-hand sides, either factoring every time (`refactor=True`) or once.

For $n = 1000$ and $k = 100$, refactoring costs about 77 times more.

## Hints

1. $\sum_{j=1}^{n-1} (j + 2j^2)$, by a loop or by the formulas for $\sum j$ and $\sum j^2$.
2. Each right-hand side needs a forward and a back substitution.
3. `lu_flops(n) / (2 * n**3 / 3)` tends to 1.
