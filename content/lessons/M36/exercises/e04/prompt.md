# The reparameterization trick

When the sample can be written as a differentiable function of the parameters and fixed noise, $x = \mu + \sigma\varepsilon$ with $\varepsilon \sim N(0, 1)$, the gradient can go through the sample (Section 4):

$$
\frac{\partial}{\partial\mu}\mathbb{E}f(x) = \mathbb{E}f'(x), \qquad \frac{\partial}{\partial\sigma}\mathbb{E}f(x) = \mathbb{E}\big[f'(x)\,\varepsilon\big] .
$$

The score-function estimator needs only $f$: $\mathbb{E}\big[f(x)\frac{x - \mu}{\sigma^2}\big]$ for $\mu$ and $\mathbb{E}\big[f(x)\big(\frac{(x - \mu)^2}{\sigma^3} - \frac1\sigma\big)\big]$ for $\sigma$.

- `reparam_samples(fprime, mu, sigma, n, rng)` and `score_samples(f, mu, sigma, n, rng)`: arrays of shape `(n, 2)` of single-sample estimates of $(\partial_\mu, \partial_\sigma)$.
- `exact_grad_square(mu, sigma)`: for $f(x) = x^2$, $\mathbb{E}f = \mu^2 + \sigma^2$, so $(2\mu, 2\sigma)$.

The tests find both estimators unbiased for $f(x) = x^2$, and the reparameterization estimator's variance far smaller.

## Hints

1. Draw $\varepsilon$ once and form $x = \mu + \sigma\varepsilon$; use the same $\varepsilon$ for both components.
2. The score of a Gaussian in $\sigma$ is the derivative of $-\log\sigma - (x - \mu)^2/(2\sigma^2)$.
3. Reparameterization needs $f$ to be differentiable and the sampler to be a differentiable function of the parameters; for a discrete choice neither holds.
