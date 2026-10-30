# A thousand equations

- `lu_fast(A)`: LU with partial pivoting where each pivot step updates the whole trailing block with **one** outer product: `U[k+1:, k:] -= np.outer(l, U[k, k:])`. Return `(perm, L, U)` with `perm` a list such that `A[perm] = L @ U`.
- `solve_fast(A, b)`: solve with `lu_fast` and two triangular solves (vectorized row by row as in e01).
- `compare(n, seed=0)`: for a random `n` by `n` system, return a dictionary with keys `"mine_s"`, `"numpy_s"` (times of `solve_fast` and `np.linalg.solve`), `"mine_res"` and `"numpy_res"` (relative residuals $\|Ax - b\| / (\|A\|\,\|x\|)$, with Frobenius norm for $A$).

Try `compare(1000)` in the console. Both residuals should sit near $10^{-16}$: pivoted elimination is **backward stable**, solving a system within rounding of the one you asked.

## Hints

1. The trailing update replaces two nested Python loops with one NumPy call per pivot.
2. Swap rows of `U` and of the computed part of `L` (columns before `k`), as in e03.
3. `time.perf_counter()` around each solve.
