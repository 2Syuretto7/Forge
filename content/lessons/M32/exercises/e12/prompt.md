# The chain that SGD runs

Gradient descent with a constant step and noisy gradients never settles at the minimum: each step is a random update of the current point, so the iterates form a Markov chain, and it converges in distribution instead (M29, Section 8). On $f(x) = \frac a2x^2$ with gradient noise of standard deviation $s$, the update $x' = x - \eta(ax + s\,z)$ is an AR(1) chain whose stationary variance solves $v = (1 - \eta a)^2v + \eta^2s^2$. The unadjusted Langevin algorithm, MALA without the correction, is the same kind of chain and has the same kind of bias.

- `sgd_chains(a, s, eta, steps, chains, rng)`: run `chains` copies in parallel from $x = 0$ for `steps` updates; return the final positions.
- `sgd_stationary_var(a, s, eta)`: $\frac{\eta s^2}{a(2 - \eta a)}$, or `math.inf` when $\eta a \ge 2$ (the chain diverges).
- `ula_chains(grad_log_p, x0, h, steps, rng)`: $x' = x + h\nabla\log\pi(x) + \sqrt{2h}\,z$ applied to the array `x0` of parallel chains.
- `ula_stationary_var(sigma2, h)`: for $\pi = N(0, \sigma^2)$, $\frac{\sigma^2}{1 - h/(2\sigma^2)}$.

The tests compare simulated variances with both formulas, show that halving a small SGD step about halves the variance around the minimum (the noise floor of M29), and that the Langevin chain without its correction overestimates the variance.

## Hints

1. Vectorize across chains: one array update per step, not a loop over chains.
2. Solve $v = (1 - \eta a)^2v + \eta^2s^2$ for $v$ and simplify.
3. For ULA on $N(0, \sigma^2)$ the update is $x' = (1 - h/\sigma^2)x + \sqrt{2h}\,z$: another AR(1) chain.
