# Covariance from a joint table

A pair of discrete random variables is given by a joint table `joint[i, j]` $= P(X = x_i, Y = y_j)$ with value arrays `xs` and `ys`.

- `marginals(joint)`: the arrays $P(X = x_i)$ and $P(Y = y_j)$.
- `covariance(joint, xs, ys)`: $\mathbb{E}[XY] - \mathbb{E}X\,\mathbb{E}Y$.
- `correlation(joint, xs, ys)`: the covariance divided by both standard deviations.
- `var_of_sum(joint, xs, ys)`: $\operatorname{Var}(X + Y)$ computed directly from the joint table, without the formula of Section 3.

The tests confirm $\operatorname{Var}(X + Y) = \operatorname{Var}X + \operatorname{Var}Y + 2\operatorname{Cov}(X, Y)$, that an independent table has covariance 0, and that the correlation, a cosine (M12), never leaves $[-1, 1]$.

## Hints

1. `joint.sum(axis=1)` sums over $j$ and gives the distribution of $X$.
2. $\mathbb{E}[XY] = \sum_{i,j} x_i y_j\,P_{ij}$ is `xs @ joint @ ys`.
3. The values of $X + Y$ are `xs[:, None] + ys[None, :]`, with probabilities `joint`.
