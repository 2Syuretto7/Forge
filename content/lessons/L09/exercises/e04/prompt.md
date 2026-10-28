# Momentum as a filter

1. `ema(xs, beta, debias=False)` returns the exponential moving average $m_t = \beta m_{t-1} + (1-\beta) x_t$ from $m_0 = 0$ for every $t = 1, \dots, n$; with `debias=True`, each $m_t$ is divided by $1 - \beta^t$.
2. `momentum_gain(beta, omega)` returns $1/|1 - \beta e^{-i\omega}|$, the steady-state amplitude of the momentum sum $v_t = \beta v_{t-1} + g_t$ for the input $g_t = \cos(\omega t)$.
3. `ema_gain(beta, omega)` returns the same for the EMA.

The tests check the gains against a simulation, so you will see momentum pass slow signals and damp the zig-zag.

## Hints

1. Python's complex numbers work with NumPy: `np.exp(-1j * omega)`.
2. The EMA is the momentum sum times $1 - \beta$.
3. A debiased EMA of a constant sequence equals that constant from the first step on.
