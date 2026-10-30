# Ten thousand small turns

Use NumPy arrays: a shape is an array of shape `(N, 2)`, one point per row.

- `rotation(theta, dtype)`: the 2 by 2 matrix that turns **row** vectors by `theta` when you compute `points @ R`, in the given float type. (For row vectors the matrix is the transpose of the one in Section 3.)
- `turn_many(points, steps, dtype)`: convert the points to `dtype`, multiply by `rotation(2 * pi / steps, dtype)` `steps` times, and return the result (a full circle in total).
- `drift(points, steps, dtype)`: the largest absolute difference between the original points and the turned ones, which in exact arithmetic would be 0.

The tests use 1,000 points and 10,000 steps, and compare float64 with float32.

## Hints

1. `np.array([[c, s], [-s, c]], dtype=dtype)`.
2. A plain loop of `X = X @ R` is fine; NumPy does the 1,000 points at once.
3. `float(np.max(np.abs(turned - points)))`.
