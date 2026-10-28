# Preferences without a reward model: DPO

An alternative alignment stage learns from preference pairs directly (L21). Implement:

1. `dpo_loss(lp_c, lp_r, ref_c, ref_r, beta)`: the mean of $-\log \sigma\bigl(\beta[(\ell_c - \ell^\text{ref}_c) - (\ell_r - \ell^\text{ref}_r)]\bigr)$ over pairs, and its gradients with respect to the policy's log-probabilities of the chosen and rejected responses.
2. `implied_reward(lp, ref, beta)`: $\beta(\ell - \ell^\text{ref})$.

## Hints

1. $-\log\sigma(m) = \log(1 + e^{-m})$: use `np.logaddexp(0, -m)`.
2. $\frac{d}{dm}[-\log\sigma(m)] = -\sigma(-m)$.
3. Pairs the policy already ranks correctly by a wide margin contribute almost no gradient.
