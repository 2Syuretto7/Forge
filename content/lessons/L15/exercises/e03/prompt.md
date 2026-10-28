# Fitting a power law

A power law $y = k x^{-a}$ is a straight line in log-log coordinates: $\log y = \log k - a \log x$.

1. `log_mse(theta, x, y)` with $\theta = (\log k, a)$: return the mean squared error between $\log k - a \log x$ and $\log y$, and its gradient with respect to $\theta$.
2. `fit_power_law(x, y)`: the least-squares fit, returning $(k, a)$.

## Hints

1. With residuals $r_i = \log k - a \log x_i - \log y_i$, the gradient is $\bigl(2\,\overline{r},\; -2\,\overline{r \log x}\bigr)$.
2. `np.polyfit(np.log(x), np.log(y), 1)` returns the slope and the intercept.
3. The least-squares fit is where the gradient of `log_mse` vanishes.
