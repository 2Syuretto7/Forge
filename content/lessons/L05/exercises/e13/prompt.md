# Break it: weight decay inside Adam

Your dictionary optimizers from exercise 8 are provided. A single weight `W` starts at 1, and its data gradient alternates $+s, -s, +s, \dots$, so on average the data does not push it anywhere and only the decay should move it.

1. `simulate(method, s, lr=0.01, wd=0.1, steps=1000)`: run Adam with `weight_decay=wd`, decoupled for `method="adamw"` and as an L2 term for `method="adam_l2"`, and return the final weight.
2. `predicted_adamw(lr, wd, steps)`: the decoupled prediction $(1 - \eta\lambda)^{\text{steps}}$.
3. `predicted_l2_noisy(s, lr, wd, steps)`: the L2 prediction when $s$ dominates: Adam divides the decay term $\lambda W$ by $\sqrt{\hat v} \approx s$, so each step removes about $\eta\lambda W/s$, giving $e^{-\text{steps}\cdot\eta\lambda/s}$.

Run both methods for $s$ from $0.01$ to $10$. AdamW decays the weight identically at every gradient scale; L2 inside Adam barely decays a weight with large gradients and wipes out one with small gradients.

## Hints

1. Keep the weight in a dictionary `{"W": np.array([1.0])}` so the optimizer treats it as a weight matrix.
2. The gradient at step `t` (from 1) is `s` when `t` is odd and `-s` when it is even.
3. For small $s$ the L2 term dominates the gradient, so Adam's step is about $\eta$ per step regardless of $W$: linear, not exponential, decay.
