# A one-dimensional tracker

A quantity drifts as a random walk, $x_t = x_{t-1} + w_t$ with $w_t \sim N(0, q)$, and you measure it with noise, $z_t = x_t + e_t$ with $e_t \sim N(0, r)$. The **Kalman filter** keeps a Gaussian belief $N(m, p)$ and alternates two steps (Section 6):

- predict: the walk adds variance, $p \leftarrow p + q$;
- update: fuse with the measurement, $K = p/(p + r)$, $m \leftarrow m + K(z_t - m)$, $p \leftarrow (1 - K)p$.

Implement:

- `kalman_1d(z, q, r, m0, p0)`: the filtered means and variances after each measurement, two arrays. Predict before every update, including the first.
- `steady_variance(q, r)`: the variance $p$ after the update once the filter has settled, the fixed point of the two steps: $p = \frac{(p + q)\,r}{p + q + r}$, which gives $p = \frac{-q + \sqrt{q^2 + 4qr}}{2}$.

## Hints

1. Loop over the measurements; the arithmetic is scalar.
2. The steady state does not depend on $m_0$ or $p_0$.
3. With $q$ much smaller than $r$ the filter averages many measurements; with $q$ much larger it trusts the last one.
