# Dot products, lengths and angles

Implement the four basic measurements of vector geometry, using only elementwise products and sums (no `np.dot`, `@` or `np.linalg`). All inputs are 1-D float arrays of the same length.

- `dot(x, y)` returns $\sum_i x_i y_i$ as a Python float.
- `norm(x)` returns $\sqrt{x^\top x}$.
- `cosine_similarity(x, y)` returns $\dfrac{x^\top y}{\|x\|\,\|y\|}$.
- `angle_degrees(x, y)` returns the angle between the vectors in degrees, in $[0, 180]$.

Rounding can push a cosine slightly outside $[-1, 1]$ for parallel vectors, which makes `arccos` return `nan`. Guard against it.

## Hints

1. `np.sum(x * y)` is a dot product.
2. Clip the cosine with `np.clip(c, -1.0, 1.0)` before calling `np.arccos`.
3. `np.degrees` converts radians to degrees.
