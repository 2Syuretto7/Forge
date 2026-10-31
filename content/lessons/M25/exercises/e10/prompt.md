# MAP with a Gaussian prior is ridge regression

Put a Gaussian prior $w \sim N(0, \tau^2 I)$ on the weights of e07's model with known noise $\sigma$. Up to constants, the negative log-posterior is

$$
\frac{1}{2\sigma^2}\lVert y - Xw\rVert^2 + \frac{1}{2\tau^2}\lVert w\rVert^2 ,
$$

so the MAP estimate is ridge regression with $\lambda = \sigma^2/\tau^2$ (Section 6).

- `neg_log_posterior(w, X, y, sigma, tau)`: the expression above.
- `ridge(X, y, lam)`: the solution of $(X^\top X + \lambda I)w = X^\top y$.
- `map_estimate(X, y, sigma, tau)`: ridge with the matching $\lambda$.

The tests confirm that the MAP minimizes the negative log-posterior, shrinks toward 0 as the prior narrows, tends to least squares as it widens, and beats least squares on new data when there are only a few noisy points.

## Hints

1. `np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)`.
2. A narrow prior (small $\tau$) means a large penalty.
3. With as many weights as data points, least squares fits the noise exactly; the prior keeps the weights modest.
