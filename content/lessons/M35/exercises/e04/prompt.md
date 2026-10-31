# Gauss-Newton for a power law with a floor

Loss curves have a floor: $L(x) = E + Ax^{-\alpha}$, where $E$ is the loss no amount of compute removes. The model is nonlinear in $\alpha$, so least squares needs iteration (Section 3). **Gauss-Newton** linearizes the model around the current $\theta = (E, A, \alpha)$ and solves the linear least-squares problem for the step: $\delta = \arg\min\lVert r - J\delta\rVert$, with residuals $r = y - L(x; \theta)$ and Jacobian $J_{ij} = \partial L(x_i)/\partial\theta_j$.

- `model(theta, x)`.
- `jacobian(theta, x)`: columns $1$, $x^{-\alpha}$, $-Ax^{-\alpha}\ln x$.
- `gauss_newton(x, y, theta0, iters=50)`: return $\theta$ after `iters` steps, or as soon as the residuals or the Jacobian stop being finite (return the last finite $\theta$ and stop).

The tests run a **gradient check** of the Jacobian against finite differences of the model and recover $\theta = (1.7, 2, 0.5)$ from 30 noisy points with a reasonable start.

## Hints

1. `np.linalg.lstsq(J, r, rcond=None)[0]` solves for the step.
2. Each Gauss-Newton step is a Newton step on the squared error with the second-derivative term of the model dropped, which is accurate when the residuals are small.
3. Use `np.errstate(all="ignore")` while testing finiteness, so overflow does not print warnings.
