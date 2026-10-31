# DPO, step 4: training recovers the KL-optimal policy

Generate preferences from a known reward with the Bradley-Terry model, train a softmax policy on the DPO loss by gradient descent, and compare it with the policy the derivation predicts, $\pi^* \propto \pi_{\text{ref}}e^{r/\beta}$ (Section 2). If the derivation is right, enough comparisons make them agree.

- `sample_preferences(r, n, rng)`: `n` pairs of distinct responses chosen uniformly, the winner drawn from Bradley-Terry; return the count matrix.
- `train_dpo(ref_logp, N, beta, steps=3000, lr=5.0)`: gradient descent on the logits from zero (reuse e03).
- `tv(p, q)`.

The tests use 8 responses, $\beta = 0.5$ and 20,000 comparisons, and find the trained policy within 0.05 of $\pi^*$ in total variation.

## Hints

1. Draw all pairs at once: `i` uniform, `j = (i + offset) % K` with a nonzero offset, and let `i` win with probability $\sigma(r_i - r_j)$; accumulate with `np.add.at`.
2. The loss is convex in the logits for a fixed comparison set, so plain gradient descent converges.
3. The remaining error comes from the finite number of comparisons, not from the optimizer.
