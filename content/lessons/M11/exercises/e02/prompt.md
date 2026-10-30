# Gaussian elimination, without pivoting

- `eliminate(A, b)`: reduce the square system to upper triangular form with the row operation "subtract multiplier times pivot row", column by column, **without** swapping rows. Return `(U, c)` as new arrays (do not modify the inputs). Raise `ValueError` if a pivot is exactly 0.
- `solve_naive(A, b)`: `eliminate`, then back substitution.

## Hints

1. Work on float copies: `U = A.astype(float)`, `c = b.astype(float)`.
2. For each pivot `k` and each row `i > k`: `m = U[i, k] / U[k, k]`, then `U[i, k:] -= m * U[k, k:]` and `c[i] -= m * c[k]`.
3. Back substitution as in e01.
