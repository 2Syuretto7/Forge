# Learning-rate schedules

Implement three schedules as functions of the step $t$ (counted from 1). All three ramp linearly from 0 to `peak` over the first `warmup` steps (rate `peak * t / warmup` while `t < warmup`), then:

1. `warmup_cosine(t, total, warmup, peak, floor=0.0)`: cosine decay from `peak` at `t = warmup` to `floor` at `t = total`, as in the derivation; stay at `floor` after `total`.
2. `warmup_linear(t, total, warmup, peak)`: linear decay to zero at `total`.
3. `inverse_sqrt(t, warmup, peak)`: `peak * sqrt(warmup / t)`, the schedule of the original transformer paper.

## Hints

1. The cosine phase uses the progress $p = (t - W)/(T - W)$ and the rate $\eta_{\min} + \tfrac12(\eta_{\max} - \eta_{\min})(1 + \cos \pi p)$.
2. Clamp the progress at 1 so the rate stays at the floor after `total`.
3. Check continuity: every schedule must give exactly `peak` at `t = warmup`.
