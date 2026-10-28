# Estimating the KL penalty

RLHF penalizes $\mathrm{KL}(\pi \,\|\, \pi_\text{ref})$, estimated from the policy's own samples. With $r = \pi_\text{ref}(y)/\pi(y)$ for a sample $y \sim \pi$:

- $k_1 = -\log r$ is unbiased but can be negative for single samples;
- $k_3 = (r - 1) - \log r$ is also unbiased (since $\mathbb{E}[r] = 1$), never negative, and usually has lower variance.

1. `kl_estimators(logp, logp_ref)`: arrays of $k_1$ and $k_3$ for each sample.
2. `exact_kl(p, q)`.

## Hints

1. Work with $\log r = \log \pi_\text{ref} - \log \pi$.
2. $x - 1 - \log x \ge 0$ for all $x > 0$.
3. The tests average both estimators over many samples and compare them with the exact value.
