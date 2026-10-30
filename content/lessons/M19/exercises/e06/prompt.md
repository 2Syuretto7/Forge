# JVPs and VJPs of a layer

For the layer $f(x) = \tanh(Ax + b)$ with $A \in \mathbb{R}^{m \times n}$, the Jacobian is $J = \operatorname{diag}(1 - y^2)\, A$ where $y = f(x)$. Implement the two products of Section 2 **without forming $J$**:

- `forward(A, b, x)` returns $y$.
- `jvp(A, b, x, v)`: $Jv$, shape `(m,)`.
- `vjp(A, b, x, u)`: $u^\top J$ as a 1-D array of shape `(n,)`.
- `full_jacobian(A, b, x)`: $J$ itself, for testing.

The identity $u^\top (J v) = (u^\top J) v$ must hold for every $u$ and $v$; the tests check it and compare with finite differences.

## Hints

1. JVP: first $A v$, then scale elementwise by $1 - y^2$.
2. VJP: first scale $u$ elementwise by $1 - y^2$, then multiply by $A^\top$.
3. Neither product needs more than one matrix-vector multiplication.
