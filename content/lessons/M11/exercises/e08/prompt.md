# How many solutions?

`classify(A, b, tol=1e-10)` returns `(kind, x)` for any system:

- `kind` is `"none"`, `"unique"` or `"infinite"`;
- `x` is a solution (with every free variable set to 0) when one exists, otherwise `None`.

Row reduce the **augmented** matrix $[A \mid b]$ with the provided `rref`. A pivot in the last column means a row $0 = 1$: no solution. Otherwise compare the number of pivots with the number of unknowns.

## Hints

1. `np.column_stack([A, b])`.
2. With free variables at 0, pivot variable `pivots[i]` equals `R[i, -1]`.
3. The puzzle's system has the solutions $(2, 1, 0) + t(-1, 0, 1)$.
