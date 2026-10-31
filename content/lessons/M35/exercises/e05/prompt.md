# Levenberg-Marquardt

Gauss-Newton trusts its linearization everywhere, and far from the answer that trust is misplaced: from a poor start the steps overshoot and the parameters fly off. **Levenberg-Marquardt** damps each step (Section 3):

$$
(J^\top J + \lambda\,\mathrm{diag}(J^\top J))\,\delta = J^\top r .
$$

Small $\lambda$ gives the Gauss-Newton step; large $\lambda$ a short step along a scaled gradient. Accept a step only if the squared error falls, then divide $\lambda$ by 3; otherwise reject it and multiply $\lambda$ by 3.

- `model`, `jacobian` as in e04, and `sse(theta, x, y)`, the sum of squared residuals (`inf` if not finite).
- `levenberg_marquardt(x, y, theta0, lam=1e-2, iters=200)`: `(theta, history)` with the accepted squared errors.
- `gauss_newton(x, y, theta0, iters=50)` as in e04, for comparison.

The tests start from $\theta_0 = (0, 0.1, 0.05)$ and $(1, 5, 3)$: Gauss-Newton ends with an infinite or huge error, Levenberg-Marquardt at the best fit.

## Hints

1. The accepted errors never increase, so `history` is non-increasing by construction.
2. Scaling the damping by $\mathrm{diag}(J^\top J)$ makes it insensitive to the units of each parameter.
3. Compute the trial loss inside `np.errstate(all="ignore")`; an overflowing trial is simply rejected.
