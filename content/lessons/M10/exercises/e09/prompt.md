# Is it linear, and what is its matrix?

- `is_linear(f, n, trials=100, seed=0)`: test numerically whether a function of vectors of length `n` (NumPy arrays) is linear: for random `x`, `y` and numbers `a`, `b`, check $f(ax + by) = a f(x) + b f(y)$ to a relative tolerance of `1e-9`.
- `matrix_of(f, n)`: the matrix whose column $j$ is $f(e_j)$.

The tests recover a hidden matrix from its map, and reject maps that only look linear.

## Hints

1. `np.random.default_rng(seed)` for reproducible tests.
2. Compare with `np.allclose(lhs, rhs, rtol=1e-9, atol=1e-12)`.
3. `np.eye(n)[j]` is $e_j$; `np.column_stack` builds the matrix.
