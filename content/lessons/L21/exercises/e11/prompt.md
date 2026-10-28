# Break it: optimizing a flawed reward

A reward model is a proxy: it agrees with true quality on typical responses and can be wrong on unusual ones, which a strong optimizer finds. The KL penalty is what keeps the policy near the responses where the proxy is trustworthy.

1. `kl_optimum(ref, reward, beta)`: $\pi \propto \pi_\text{ref} e^{r/\beta}$.
2. `tradeoff(ref, proxy, truth, betas)`: for each $\beta$, optimize the proxy and return (KL to the reference, expected proxy reward, expected true reward).

## Hints

1. Work with logits $\log \pi_\text{ref} + r/\beta$ and a stable softmax.
2. As $\beta$ falls, KL and the proxy reward both rise; the true reward rises, then falls.
3. This rise-then-fall of true quality against KL is the reward-model overoptimization measured by Gao et al. (2023).
