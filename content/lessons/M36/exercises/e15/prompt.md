# Break it: optimizing a proxy

In RLHF the reward is a learned model, a **proxy** for what people want, and it is wrong in places. Maximizing it without restraint finds those places (Section 7). The KL-regularized objective $\mathbb{E}_\pi[\hat r] - \beta\,\mathrm{KL}(\pi\,\|\,\pi_{\text{ref}})$ has the closed-form optimum $\pi^* \propto \pi_{\text{ref}}\,e^{\hat r/\beta}$ (M30), which stays close to the reference policy where the proxy's evidence is weak.

- `kl_optimal(pi_ref, r_hat, beta)`: $\pi^*$.
- `kl(p, q)`: $\sum_ip_i\log(p_i/q_i)$.
- `true_reward(pi, r)`: $\sum_i\pi_ir_i$.
- `sweep(pi_ref, r_hat, r, betas)`: for each $\beta$, the pair `(true reward, KL from the reference)`.

The tests use 20 responses whose proxy reward equals the true reward plus a small error, except one: the proxy scores the truly worst response just above the best. As $\beta \to 0$ the policy collapses onto that response and the true reward falls below the reference policy's; an intermediate $\beta$ beats both extremes.

## Hints

1. Compute $\log\pi_{\text{ref}} + \hat r/\beta$ and normalize with a stable softmax.
2. As $\beta \to \infty$, $\pi^* \to \pi_{\text{ref}}$; as $\beta \to 0$, it puts all its mass on the proxy's best response.
3. The RewardKLTradeoff widget draws the same curve.
