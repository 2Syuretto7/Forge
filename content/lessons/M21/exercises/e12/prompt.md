# Temperature scaling

Divide every log-odds by a temperature $T$ and fit $T$ on held-out data by minimizing the negative log-likelihood

$$
\text{NLL}(T) = -\frac1N \sum_i \big[y_i \log \sigma(z_i/T) + (1 - y_i)\log(1 - \sigma(z_i/T))\big] .
$$

- `nll(z, y, T)`: that loss, computed stably with `np.logaddexp`: $-\log\sigma(u) = \log(1 + e^{-u})$.
- `dnll_dT(z, y, T)`: its derivative, $\frac{1}{N}\sum_i (\sigma(z_i/T) - y_i)\cdot(-z_i/T^2)$.
- `fit_temperature(z, y)`: minimize over $T \in [0.25, 10]$ by bisection on the sign of the derivative (the loss is unimodal in $T$ here).

The tests run a **gradient check** of `dnll_dT` and fit a temperature above 1 to overconfident log-odds, reducing the calibration error.

## Hints

1. $\log(1 - \sigma(u)) = -\log(1 + e^{u})$.
2. The derivative of $\sigma(u)$ is $\sigma(1 - \sigma)$; the chain rule gives the formula.
3. Bisect on $[0.25, 10]$ for 60 steps.
