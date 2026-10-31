# Capstone: a Gaussian toolkit and a tracker

Part 1, the toolkit, for vectors stored as rows:

1. `sample(mu, Sigma, n, rng)` by the Cholesky factor.
2. `logpdf(X, mu, Sigma)` through the Cholesky factor, finite in 256 dimensions.
3. `condition(mu, Sigma, obs, x_obs)`: the conditional mean and covariance of the unobserved coordinates.

Part 2, the tracker. The starter's `simulate_target(n, seed)` moves a target along a line with nearly constant velocity: each step, a random acceleration $a_t \sim N(0, 0.02^2)$ changes the velocity by $a_t$ and the position by $v_t + a_t/2$. You see only the position, with noise of standard deviation 1. It returns the true positions and the measurements.

4. `track(z, accel_sd=0.02, meas_sd=1.0)`: a Kalman filter on the state $(\text{position}, \text{velocity})$ with $F = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, process covariance $Q = \sigma_a^2\, g g^\top$ with $g = (\frac12, 1)$, measurement $H = (1, 0)$ and $R = \sigma_m^2$. Start from the mean $(z_0, 0)$ and covariance $\mathrm{diag}(\sigma_m^2, 100)$, update with $z_0$, then predict and update for each later measurement. Return the filtered positions.

The tests check the toolkit against explicit formulas, and require the tracker's root-mean-square position error, after the first 50 steps, to be **less than half** that of the raw measurements on 2,000 steps.
