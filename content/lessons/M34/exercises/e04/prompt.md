# The Johnson-Lindenstrauss projector

Multiply $n$ points in $\mathbb R^d$ by a random $d \times k$ matrix $R$ with independent $N(0, 1/k)$ entries. Every squared distance is preserved in expectation, and with high probability all of them to within a factor $1 \pm \varepsilon$ once $k \ge \frac{4\ln n}{\varepsilon^2/2 - \varepsilon^3/3}$, whatever $d$ is (Section 4).

- `jl_matrix(d, k, rng)`.
- `pairwise_sq_dists(X)`: the $n \times n$ matrix of squared distances, from the Gram matrix: $\lVert x_i\rVert^2 + \lVert x_j\rVert^2 - 2x_i\cdot x_j$, clipped at 0.
- `max_sq_distortion(X, Y)`: $\max_{i < j}\left\lvert\frac{\lVert y_i - y_j\rVert^2}{\lVert x_i - x_j\rVert^2} - 1\right\rvert$.
- `jl_dim(n, eps)`: the bound on $k$ above, rounded up.

The tests project 200 points from 1,000 dimensions to the dimension the lemma asks for at $\varepsilon = 0.3$ and find every one of the 19,900 squared distances within the bound.

## Hints

1. `np.triu_indices(n, 1)` lists the pairs $i < j$.
2. Scale the Gaussian entries by $1/\sqrt k$ so that $\mathbb{E}\lVert R^\top x\rVert^2 = \lVert x\rVert^2$.
3. The bound does not mention $d$: it depends only on the number of points and the accuracy.
