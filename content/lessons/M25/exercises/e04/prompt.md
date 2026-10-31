# Gaussian maximum likelihood with an unconstrained parameter

Optimizers prefer unconstrained parameters, so parametrize the Gaussian by $\mu$ and $s = \log \sigma$. For data `x` (1-D array), the **average** negative log-likelihood is

$$
J(\mu, s) = \frac{1}{2}\log(2\pi) + s + \frac{1}{2n}\sum_i (x_i - \mu)^2 e^{-2s}.
$$

- `nll(mu, s, x)` returns $J$ as a float.
- `grad_nll(mu, s, x)` returns `np.array([dJ/dmu, dJ/ds])`.
- `mle(x)` returns `(mu_hat, sigma_hat)` in closed form, with $\hat\sigma^2 = \frac{1}{n}\sum_i (x_i - \bar x)^2$.

Derive the two partial derivatives yourself before coding; the test checks them against finite differences and checks that they vanish at the MLE.

## Hints

1. $\partial J/\partial \mu = -\frac{1}{n}\sum_i (x_i - \mu) e^{-2s}$.
2. $\partial J/\partial s = 1 - \frac{1}{n}\sum_i (x_i - \mu)^2 e^{-2s}$.
3. `np.std(x)` uses the $1/n$ convention by default (`ddof=0`).
