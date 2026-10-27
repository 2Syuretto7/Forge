# A numerical Hessian

The Hessian $H_{ij} = \partial^2 f/\partial x_i \partial x_j$ is the Jacobian of the gradient. Build it by central differences of an analytic gradient, then symmetrize.

- `hessian_from_grad(grad, x, h)`: column $j$ is $\big(\nabla f(x + h e_j) - \nabla f(x - h e_j)\big)/(2h)$; return $\tfrac12(H + H^\top)$.
- `is_local_min(H, tol)`: `True` if every eigenvalue exceeds `tol`.
- `curvature_bound(H)`: the largest eigenvalue, which is the $L$ of the descent lemma.

## Hints

1. Reuse your numerical Jacobian idea on the gradient function.
2. `np.linalg.eigvalsh` for symmetric matrices.
3. Symmetrizing removes the small asymmetry rounding introduces.
