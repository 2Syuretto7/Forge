# Sketched least squares

A tall least-squares problem, $m \gg n$, can be shrunk before it is solved: multiply both $A$ and $b$ by a random $s \times m$ matrix $S$ with independent $N(0, 1/s)$ entries and solve the small problem $\min_x\lVert S(Ax - b)\rVert$ (Section 6). A Gaussian sketch preserves the lengths of all vectors in the $(n + 1)$-dimensional span of $A$'s columns and $b$ up to a factor near 1, so the sketched solution's residual is close to the best one; for Gaussian sketches the expected squared ratio is about $1 + \frac n{s - n - 1}$.

- `sketch(A, b, s, rng)`: `(SA, Sb)`.
- `sketched_lstsq(A, b, s, rng)`: the solution of the sketched problem (`np.linalg.lstsq`).
- `residual_ratio(A, b, x)`: $\lVert Ax - b\rVert/\lVert Ax^* - b\rVert$ with $x^*$ the exact least-squares solution.
- `predicted_ratio(n, s)`: $\sqrt{1 + n/(s - n - 1)}$.

The tests sketch a $5{,}000 \times 30$ problem down to 100 and 300 rows and find the residual within the prediction.

## Hints

1. Scale the Gaussian entries by $1/\sqrt s$ so that $\mathbb{E}\lVert Sv\rVert^2 = \lVert v\rVert^2$.
2. The sketch size must exceed $n$, or the small problem is underdetermined.
3. A dense Gaussian sketch costs as much as solving the problem; fast transforms and sparse sketches make the same idea cheap at scale.
