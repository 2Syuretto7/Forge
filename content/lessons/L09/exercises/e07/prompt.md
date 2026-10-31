# Rotary position embeddings

Implement `rope(X, positions, base=10000.0)`: for each row $p$ (at position `positions[p]`) and each pair of columns $(2i, 2i + 1)$, rotate the pair by the angle $p\,\theta_i$ with $\theta_i = \text{base}^{-2i/d}$:
$$
(x_{2i}, x_{2i+1}) \mapsto (x_{2i}\cos\phi - x_{2i+1}\sin\phi,\; x_{2i}\sin\phi + x_{2i+1}\cos\phi).
$$
The tests check that the result preserves norms, and that the score between a rotated query and a rotated key depends only on the difference of their positions.

## Hints

1. Angles: `positions[:, None] * theta[None, :]`, shape `(n, d/2)`.
2. Take `x0 = X[:, 0::2]` and `x1 = X[:, 1::2]`, and write the two results back into the same columns.
3. Position 0 leaves a row unchanged.
