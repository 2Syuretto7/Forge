# The Ornstein-Uhlenbeck process

The **Ornstein-Uhlenbeck** process $dX = -\theta(X - \mu)\,dt + \sigma\,dW$ is pulled toward $\mu$ and kicked by noise (Section 2). It is solved exactly: given $X_0$, $X_t$ is normal with mean $\mu + (X_0 - \mu)e^{-\theta t}$ and variance $\frac{\sigma^2}{2\theta}(1 - e^{-2\theta t})$, so as $t \to \infty$ every start forgets itself and the process settles into the stationary $N(\mu, \sigma^2/(2\theta))$, with autocorrelation $e^{-\theta\tau}$ at lag $\tau$. The forward process of a diffusion model is this, with $\theta = 1$, $\mu = 0$, $\sigma = \sqrt2$.

- `ou_mean_var(x0, t, theta, mu, sigma)`: the exact mean and variance.
- `ou_exact_step(x, dt, theta, mu, sigma, rng)`: one exact transition for an array of states.
- `ou_path(x0, n, dt, theta, mu, sigma, rng)`: a path of length $n$ by exact steps.
- `stationary_var(theta, sigma)`.

The tests check the moments against simulation, the stationary variance and the autocorrelation of a long path.

## Hints

1. The exact step is $X_{t+dt} = \mu + (X_t - \mu)e^{-\theta dt} + \sqrt{v}\,z$ with $v$ the variance after time $dt$ from a fixed start.
2. The lag-$k$ autocorrelation of the sampled path is $e^{-\theta k\,dt}$.
3. Exact steps are stable for any $dt$; e13 shows that Euler-Maruyama is not.
