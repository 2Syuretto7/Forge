# Langevin proposals

Random-walk proposals ignore the shape of the target. The **Metropolis-adjusted Langevin algorithm** (MALA) proposes a step of the Langevin diffusion, $y = x + h\nabla\log\pi(x) + \sqrt{2h}\,z$, which drifts uphill in density, and corrects with Metropolis-Hastings because the proposal is not symmetric: $\log q(y \mid x) = -\lVert y - x - h\nabla\log\pi(x)\rVert^2/(4h)$ plus a constant (Section 8).

- `log_gauss(x, scales)` and `grad_log_gauss(x, scales)`: an independent Gaussian with standard deviations `scales`, up to a constant.
- `mala_chain(log_p, grad_log_p, x0, h, n, rng)`: `(samples, acceptance)`.
- `tune_mala(log_p, grad_log_p, x0, rng, h=0.01, target=0.574, rounds=30, per_round=200)`: as e10's tuner, aiming at MALA's optimal acceptance 0.574. Return `(h, x)`.

The tests run a **gradient check**, confirm that MALA samples the right variances, and race it against tuned random-walk Metropolis in 50 dimensions, measuring each by the worst coordinate's effective sample size.

## Hints

1. The acceptance log ratio is $\log\pi(y) - \log\pi(x) + \log q(x \mid y) - \log q(y \mid x)$; the constants of $q$ cancel.
2. Keep the gradient at the current state, as you keep its log density, so each step costs one new gradient.
3. The optimal step shrinks like $d^{-1/3}$ for MALA but like $d^{-1/2}$ for the random walk, which is the source of the speed-up.
