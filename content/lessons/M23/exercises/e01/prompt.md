# Joint, marginal and conditional tables

A pair of discrete variables is given by a joint table `joint[i, j]` $= P(X = i, Y = j)$ (Section 1).

- `marginal(joint, axis)`: the distribution of $X$ (`axis=0`) or of $Y$ (`axis=1`).
- `conditional_y_given_x(joint)`: the table `c[i, j]` $= P(Y = j \mid X = i)$; each row sums to 1. Raise `ValueError` if some $P(X = i)$ is 0.
- `is_independent(joint, tol=1e-12)`: whether the table equals the outer product of its marginals.
- `from_conditional(px, cond)`: rebuild the joint table from the distribution of $X$ and the conditional table, $P(X = i, Y = j) = P(X = i)\,P(Y = j \mid X = i)$.

## Hints

1. `axis=0` means "the distribution of the first variable": sum over the second index, `joint.sum(axis=1)`.
2. Divide each row by its sum with broadcasting: `joint / px[:, None]`.
3. `np.outer(px, py)` is the independent table with the same marginals.
