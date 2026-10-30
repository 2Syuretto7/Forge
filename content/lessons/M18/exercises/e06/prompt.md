# A numerical Hessian

The Hessian is the Jacobian of the gradient. Build it by central differences of an analytic gradient, then symmetrize.

- `hessian_from_grad(grad, x, h=1e-5)`: column $j$ is $\big(\nabla f(x + h e_j) - \nabla f(x - h e_j)\big)/(2h)$; return $\frac12(H + H^\top)$.
- `is_local_min(H, tol=1e-8)`: whether every eigenvalue exceeds `tol`.
- `curvature_bound(H)`: the largest eigenvalue, the $L$ of the descent lemma.

The tests run **gradient checks** on a quadratic, a saddle and the Rosenbrock function.

## Hints

1. Reuse the numerical Jacobian idea on the gradient function.
2. `np.linalg.eigvalsh` for symmetric matrices.
3. Symmetrizing removes the small asymmetry that rounding introduces.
