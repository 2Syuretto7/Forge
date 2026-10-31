# The retransformation bias

A fit in log space predicts the median of $y$, not its mean: if $\log y = \log\mu + \varepsilon$ with $\varepsilon \sim N(0, \sigma^2)$, then $\mathbb{E}y = \mu e^{\sigma^2/2}$ (Section 2). Exponentiating the fitted line underestimates the average by that factor. Duan's **smearing** estimate fixes it without assuming normality: multiply by the average of $e^{\text{residual}}$.

- `lognormal_mean_factor(sigma)`: $e^{\sigma^2/2}$.
- `naive_mean_prediction(A, alpha, x)`: $Ax^{-\alpha}$.
- `smearing_factor(residuals)`: the mean of $e^{r}$ over the log-space residuals.
- `log_residuals(x, y, A, alpha)`: $\log y - \log(Ax^{-\alpha})$.

The tests fit noisy data with $\sigma = 0.4$, show the naive prediction about 8 percent below the true mean, and the smeared one within 2 percent.

## Hints

1. $\mathbb{E}e^{\varepsilon} = e^{\sigma^2/2}$ is the moment generating function of a normal at $t = 1$ (M24).
2. With $\sigma = 0.4$ the factor is $e^{0.08} \approx 1.083$.
3. A loss averaged over many sequences is a mean, so this bias matters whenever a model is fitted in log space and read in linear space.
