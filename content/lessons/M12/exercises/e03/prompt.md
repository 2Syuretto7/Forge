# Modified Gram-Schmidt

`gram_schmidt(A)` for `A` of shape `(m, n)` with $m \geq n$: return `Q` of shape `(m, n)` with orthonormal columns spanning the same space, built in order (`Q[:, 0]` is `A[:, 0]` normalized, and so on).

Use the **modified** form: keep a working copy `v` of column `k` and subtract its projection onto each earlier `q_j` one at a time, recomputing the coefficient from the current `v`:

```
v = A[:, k]
for j in range(k):
    v = v - (Q[:, j] @ v) * Q[:, j]
```

If a column depends on earlier ones, the remainder is nearly zero: raise `ValueError` when `norm(v) < 1e-10 * norm(A[:, k])`.

## Hints

1. Work in float64 with `Q = np.zeros((m, n))`.
2. The coefficient uses the updated `v`, not the original column.
3. Normalize after the inner loop.
