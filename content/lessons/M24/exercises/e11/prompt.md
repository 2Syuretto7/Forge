# The gradient of an expectation, two ways

Training often needs $\frac{d}{d\theta}\mathbb{E}_{x \sim N(\theta, 1)}[f(x)]$. Two Monte Carlo estimators exist, and M36 builds on both:

- **pathwise**: write $x = \theta + z$ with $z$ standard normal; then the derivative is $\mathbb{E}[f'(\theta + z)]$.
- **score function**: differentiate the density instead; the derivative is $\mathbb{E}[f(x)\,(x - \theta)]$, which needs only values of $f$.

Implement both, each drawing `z = rng.standard_normal(n)` once and returning `(estimate, standard_error)`:

- `pathwise_grad(fprime, theta, n, rng)`.
- `score_grad(f, theta, n, rng)`.

The tests run a **gradient check**: both estimates must agree, within 4 standard errors, with the derivative of the exact expectation computed by finite differences, for $f(x) = x^2$ (where $\mathbb{E}f = \theta^2 + 1$) and $f(x) = \sin x$ (where $\mathbb{E}f = e^{-1/2}\sin\theta$). The pathwise estimator should have the smaller error bar.

## Hints

1. $x = \theta + z$, so $x - \theta = z$.
2. The score of $N(\theta, 1)$ is $\frac{\partial}{\partial\theta}\log p(x) = x - \theta$.
3. The score-function terms $f(x)z$ are large when $f$ is large, even where $f$ barely changes with $\theta$.
