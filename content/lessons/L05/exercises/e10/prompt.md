# Break it: unscaled features

Measure Section 5's prediction: badly scaled features make gradient descent slow, standardization fixes it.

- `hessian_condition(X)`: the condition number of $\tfrac2n X^\top X$.
- `steps_to_converge(X, y, tol, max_steps)`: run gradient descent on $\tfrac1n\|Xw - y\|^2$ from zero with learning rate $0.9 \times 2/\lambda_{\max}$ and return the number of steps until $\|w - w^\star\| \le \text{tol}\cdot\|w^\star\|$, where $w^\star$ is the least-squares solution. Return `max_steps` if it never gets there.
- `standardize(X)`: subtract column means and divide by column standard deviations.

## Hints

1. $w^\star$ from `np.linalg.lstsq`.
2. Check the stopping condition before each step.
3. Fit the standardized problem with an intercept-free model: standardization removes the need for one when `y` is also centered, which the test does.
