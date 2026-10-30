# Expanding the square

For $L(x) = \|Ax - b\|^2$, Section 3 expanded $L(x + tu) = L(x) + t\,(s \cdot u) + t^2 \|Au\|^2$ with $s = 2A^\top(Ax - b)$.

- `loss(x, A, b)`: $L(x)$ as a float.
- `slope_vector(x, A, b)`: $s$.
- `step_down(A, b, steps)`: start at $x = 0$ and repeat $x \leftarrow x - \eta\, s(x)$ with $\eta = 1 / (2\|A\|_F^2)$, where $\|A\|_F^2$ is the sum of the squares of all entries. Return `x`.

The tests check an **invariant**: the expansion is exact, for random $x$, $u$ and $t$, and the steps reach the least-squares solution. M18 calls $s$ the gradient and M29 studies the step size; this step is small enough to be safe for any $A$.

## Hints

1. `r = A @ x - b`, then `r @ r` and `2 * A.T @ r`.
2. `np.sum(A * A)`.
3. Each step lowers $L$, because $t\,(s \cdot u)$ with $u = -s$ is negative and the $t^2$ term is smaller for this $\eta$.
