# Ellipses of equal density

The density of $N(\mu, \Sigma)$ depends on $x$ only through the **Mahalanobis distance** $r = \sqrt{(x - \mu)^\top \Sigma^{-1} (x - \mu)}$, so its contours are ellipses (Section 3).

- `ellipse_axes(Sigma)`: the eigenvalues of $\Sigma$ in decreasing order and the matching unit eigenvectors as columns; the half-axes of the contour $r = k$ are $k\sqrt{\lambda_i}$ along them.
- `mahalanobis(X, mu, Sigma)`: $r$ for each row of `X`.
- `prob_inside(k)`: in two dimensions, the probability of $r \le k$, which is $1 - e^{-k^2/2}$.
- `ellipse_points(mu, Sigma, k, m=100)`: `m` points on the contour $r = k$, as an `(m, 2)` array.

The tests sample 200,000 points and compare the fractions inside the 1-, 2- and 3-sigma ellipses with `prob_inside`.

## Hints

1. `np.linalg.eigh` returns increasing eigenvalues; reverse both outputs.
2. Map the unit circle: $x = \mu + V\,\mathrm{diag}(k\sqrt{\lambda})\,(\cos t, \sin t)$.
3. In polar coordinates the standard 2D Gaussian's radius has density $r e^{-r^2/2}$, whose integral from 0 to $k$ gives `prob_inside`.
