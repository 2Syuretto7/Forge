# Lagrange multipliers for equality constraints

To minimize $f(x)$ subject to $Cx = d$, look for points where $\nabla f$ is a combination of the constraint normals: $\nabla f(x) + C^\top\lambda = 0$ (Section 6). For a quadratic $f(x) = \frac12 x^\top A x - b^\top x$ with $A$ positive definite, that condition and the constraint form one linear system,

$$
\begin{pmatrix} A & C^\top \\ C & 0 \end{pmatrix}\begin{pmatrix} x \\ \lambda \end{pmatrix} = \begin{pmatrix} b \\ d \end{pmatrix} .
$$

- `solve_equality_qp(A, b, C, d)`: return `(x, lam)` from that system.
- `objective(A, b, x)`.
- `projected_minimum_check(A, b, C, d, x, trials, rng)`: the smallest increase of the objective over `trials` random feasible points $x + Nz$, where the columns of $N$ span the null space of $C$ (from `np.linalg.svd`); positive means $x$ is the constrained minimum.

The tests solve the closest point to the origin on a line, minimize a quadratic on a plane, and check the multiplier's meaning: the rate at which the optimal value changes as the constraint level $d$ moves.

## Hints

1. `np.block([[A, C.T], [C, np.zeros((m, m))]])`.
2. The null space of $C$ ($m$ by $n$, rank $m$): the last $n - m$ rows of $V^\top$ in the SVD.
3. With the sign convention here, $\frac{\partial f^\star}{\partial d} = -\lambda$.
