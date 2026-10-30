# A saddle in disguise

For $f(x, y) = x^2 + y^2 - 3xy$:

- `axis_check(f, x0, t=1e-2)`: whether $f$ rises when $x_0$ moves by $\pm t$ along each coordinate axis, four evaluations: the test a hurried person might trust.
- `hessian_eigen(H)`: eigenvalues and eigenvectors (`np.linalg.eigh`).
- `escape_direction(H)`: the unit eigenvector of the most negative eigenvalue, or `None` if there is none.

The tests show `axis_check` passing at the origin, the Hessian revealing a negative eigenvalue, and $f$ falling along the escape direction.

## Hints

1. Compare $f(x_0 \pm t e_i)$ with $f(x_0)$.
2. The Hessian is constant here: $\begin{pmatrix} 2 & -3 \\ -3 & 2 \end{pmatrix}$.
3. `eigh` sorts eigenvalues in increasing order.
