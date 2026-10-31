# Break it: Adam without bias correction

Your single-array `Adam` from exercise 5 is provided.

1. `uncorrected_factor(t, b1=0.9, b2=0.999)`: by how much step $t$ grows when the bias correction is removed, $(1 - \beta_1^t)/\sqrt{1 - \beta_2^t}$, for a scalar or an array of steps.
2. `peak(b1=0.9, b2=0.999, tmax=10000)`: the step in $1, \dots, t_{\max}$ where that factor is largest, and its value.
3. `measured_factor(t, b1=0.9, b2=0.999, g=1.0)`: run Adam with and without correction (use `eps=0`) on the constant gradient `g` for `t` steps, and return the ratio of the sizes of their `t`-th steps.

## Hints

1. With a constant gradient, $m_t = (1 - \beta_1^t) g$ and $v_t = (1 - \beta_2^t) g^2$ exactly, so the corrected step is always $\eta$.
2. `np.argmax` over an array of factors for `t = 1..tmax` finds the peak.
3. The step size is the absolute change of `x` in that step.
