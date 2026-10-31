# Predicting the number of iterations

If the error shrinks by at least $\rho$ per step, reaching a relative error $\varepsilon$ takes at most

$$
k = \left\lceil \frac{\log\varepsilon}{\log\rho} \right\rceil \approx \frac{\kappa}{c}\log\frac1\varepsilon
$$

steps, with $c = 1$ for the step $1/L$ and $c = 2$ for the best step (Section 4): the iteration count grows in proportion to the condition number.

- `iterations_bound(kappa, eps, step="best")`: $k$ from $\rho = \frac{\kappa - 1}{\kappa + 1}$ (`"best"`) or $\rho = 1 - 1/\kappa$ (`"inverse_L"`).
- `iterations_needed(A, b, x0, step, eps, max_iter=10**6)`: run gradient descent until $\lVert x_k - x^\star\rVert \le \varepsilon\lVert x_0 - x^\star\rVert$ and return $k$.

The tests check that the bound holds, that it is nearly tight when the start has a component along the slowest direction, and that ten times the condition number costs about ten times the iterations.

## Hints

1. `math.ceil(math.log(eps) / math.log(rho))`.
2. Use e06's update; stop as soon as the error is small enough.
3. With the best step both extreme eigenvalues contract at the same rate $\rho$, so either end of the spectrum can be the slow one.
