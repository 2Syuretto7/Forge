# Norms concentrate

A vector $x \in \mathbb R^d$ with independent standard normal entries has $\lVert x\rVert^2 = \sum_ix_i^2$, a sum of $d$ independent terms with mean 1 and variance 2, so $\mathbb{E}\lVert x\rVert^2 = d$ and $\operatorname{Var}\lVert x\rVert^2 = 2d$ (Section 1). The length itself is close to $\sqrt d$, with a spread that does not grow: $\operatorname{sd}\lVert x\rVert \to 1/\sqrt2$.

- `random_vectors(n, d, rng)`: an $n \times d$ array of standard normals.
- `norm_stats(d, n, rng)`: the mean of $\lVert x\rVert/\sqrt d$ and the standard deviation of $\lVert x\rVert$ over $n$ vectors, as a tuple.
- `shell_fraction(d, n, rng, width=0.1)`: the fraction of vectors whose length lies within `width` times $\sqrt d$ of $\sqrt d$.

The tests find the relative spread shrinking like $1/\sqrt d$ and nearly every vector in 1,000 dimensions on a thin shell.

## Hints

1. `np.linalg.norm(X, axis=1)`.
2. In 2 dimensions the length is spread widely; in 1,000 it is pinned near $\sqrt{1000} \approx 31.6$ with spread about $0.71$.
3. A Gaussian's mass is not near its peak at the origin but on this shell, where volume and density balance.
