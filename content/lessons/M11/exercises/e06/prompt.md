# Reduced row echelon form

`rref(A, tol=1e-10)` returns `(R, pivots)`:

- `R` is the **reduced** row echelon form: each pivot is 1, it is the only nonzero entry in its column, and pivots move right as you go down;
- `pivots` is the list of pivot column indices.

Use partial pivoting within each column (the largest entry at or below the current row), and treat entries at most `tol` as zero.

## Hints

1. Keep a current row `r`; for each column `j`, find the best pivot at or below `r`; skip the column if it is negligible.
2. Swap it into row `r`, divide row `r` by the pivot, and subtract multiples of row `r` from **every** other row, above and below.
3. Set tiny leftovers to exactly 0 at the end with `R[np.abs(R) < tol] = 0`.
