# DPO, break it: preferences without noise

The derivation assumed Bradley-Terry: every comparison could have gone either way. If one response always wins, the maximum-likelihood reward difference is infinite, and the DPO loss is minimized only by sending the probability ratio to infinity, whatever $\beta$ is (Section 5). The KL term that was supposed to keep the policy near the reference has disappeared from the loss.

- `train_dpo(ref_logp, N, beta, steps, lr=5.0)`: as e04, returning the logits.
- `prob_gap(z)`: the largest probability minus the second largest.
- `loss_at(z, ref_logp, N, beta)`: e03's loss.

The tests give response 0 every win against response 1 and nothing else, and find the loss still falling and the gap still growing after 1,000, 5,000 and 20,000 steps: there is no optimum to converge to.

## Hints

1. With $N_{01} > 0$ and $N_{10} = 0$, the loss is $\log(1 + e^{-h})$, which decreases toward 0 as $h \to \infty$ and never attains it.
2. Track the logits' difference: it keeps increasing, roughly logarithmically in the number of steps.
3. Practical DPO adds label smoothing or early stopping for this reason; the derivation's assumption failed, not the optimizer.
