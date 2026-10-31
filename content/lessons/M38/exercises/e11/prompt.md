# Adam, step 1: the update and its bias correction

Adam keeps exponential averages of the gradient and of its square, $m_t = \beta_1m_{t-1} + (1 - \beta_1)g_t$ and $v_t = \beta_2v_{t-1} + (1 - \beta_2)g_t^2$, both started at 0, and steps by $-\eta\,\hat m_t/(\sqrt{\hat v_t} + \varepsilon)$ with the **bias corrections** $\hat m_t = m_t/(1 - \beta_1^t)$ and $\hat v_t = v_t/(1 - \beta_2^t)$ (Section 4, M29). Started at zero, $\mathbb{E}m_t = (1 - \beta_1^t)\mathbb{E}g$ for a stationary gradient, which the correction undoes.

- `adam_step(x, g, state, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8)`: one update; `state` is a dict with `"m"`, `"v"` and `"t"` (start with zeros and 0), updated in place; return the new `x`.
- `first_step_size(g, lr)`: the size of Adam's first update for gradient `g`, which the derivation says is $\eta$ per coordinate (up to $\varepsilon$), whatever the gradient's scale.

The tests confirm the first step is $\eta\,\mathrm{sign}(g)$, and that the corrected averages are unbiased for a constant gradient at every step.

## Hints

1. At $t = 1$: $\hat m = g$ and $\hat v = g^2$, so the update is $\eta\,g/\lvert g\rvert$.
2. Increment `t` before computing the corrections.
3. The correction matters most in the first few hundred steps, when $\beta_2^t$ is far from 0.
