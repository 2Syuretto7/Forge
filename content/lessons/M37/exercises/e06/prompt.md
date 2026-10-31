# Denoising score matching

The score of the noised data is unknown when the data distribution is, but a regression target for it is known (Section 6). If $x_t = ax_0 + \sigma\varepsilon$, the conditional score is $\nabla\log p(x_t \mid x_0) = -\varepsilon/\sigma$, and minimizing

$$
\mathbb{E}\,\big\lVert s(x_t) + \varepsilon/\sigma\big\rVert^2
$$

over functions $s$ gives the true marginal score $\nabla\log p_t$, because a conditional expectation minimizes a squared error (M22). Fit a model linear in its parameters, $s(x) = \sum_jc_j\phi_j(x)$, by least squares on samples.

- `features(x)`: the columns $1, x, x^3, \tanh(x - 1.5), \tanh(x + 2)$ and $\tanh(2(x - 1.5))$, $\tanh(2(x + 2))$.
- `dsm_data(x0, t, rng)`: `(x_t, target)` with target $-\varepsilon/\sigma$ for the forward process of e05.
- `dsm_loss(c, X, target)`: the mean squared error of `features(X) @ c`, and `grad_dsm_loss(c, X, target)`.
- `fit_score(X, target)`: the least-squares coefficients.

The tests run a **gradient check** of the loss, then fit on noised samples of e05's mixture at $t = 0.3$ and find the fitted score close to the exact noised score of e04 where the data are.

## Hints

1. The gradient of $\frac1n\lVert\Phi c - y\rVert^2$ is $\frac2n\Phi^\top(\Phi c - y)$.
2. `np.linalg.lstsq(Phi, target, rcond=None)[0]`.
3. Individual targets are hopelessly noisy, of size $1/\sigma$; their conditional average is the smooth score. Regression does the averaging.
