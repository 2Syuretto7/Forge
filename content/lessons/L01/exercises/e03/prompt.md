# Modified Gram-Schmidt

Implement `gram_schmidt(A)` for `A` of shape `(m, n)` with $m \ge n$. Return `Q` of shape `(m, n)` whose columns are orthonormal and span the same space as the columns of `A`, built in order: `Q[:, 0]` is `A[:, 0]` normalized, `Q[:, 1]` comes from `A[:, 1]`, and so on.

Use the **modified** form: keep a working copy `v` of column `k` and subtract its projection onto each earlier `q_j` one at a time, recomputing the coefficient from the current `v`:

```
v = A[:, k]
for j in range(k):
    v = v - (Q[:, j] @ v) * Q[:, j]
```

The classical form computes every coefficient from the original column. Both are exact in real arithmetic; only the modified one keeps orthogonality on nearly parallel columns, and one test checks this.

If a column is (numerically) dependent on earlier ones, its remainder has length near zero. Raise `ValueError` when `norm(v) < 1e-10 * norm(A[:, k])`.

## Hints

1. Work in float64: `Q = np.zeros((m, n))`.
2. The coefficient must use the updated `v`, not the original column.
3. Normalize with `v / np.linalg.norm(v)` after the inner loop.
