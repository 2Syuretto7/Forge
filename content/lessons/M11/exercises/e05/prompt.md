# Rank by elimination

`rank(A, tol=None)` for any `m` by `n` matrix:

- use **complete pivoting**: at step $k$, bring the largest absolute entry of the remaining block (rows and columns $k$ and beyond) to position $(k, k)$ by swapping a row and a column, then clear below it;
- stop when that largest entry is at most `tol`; the number of pivots used is the rank;
- by default `tol = max(m, n) * 1e-12 * max|a_ij|` (and rank 0 for a zero matrix).

The tests check an **invariant**: on random matrices built with a known rank, `rank(A)` and `rank(A.T)` both equal that rank.

## Hints

1. `np.unravel_index(np.argmax(np.abs(B)), B.shape)` finds the largest entry of a block.
2. Swapping columns permutes the unknowns, which does not change the rank.
3. A product of an `m` by `r` and an `r` by `n` random matrix has rank `r`.
