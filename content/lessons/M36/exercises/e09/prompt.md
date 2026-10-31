# REINFORCE on a bandit

Learn which of $K$ slot machines pays best by sampling: a softmax policy over arms, a stochastic reward from the chosen arm, and a REINFORCE step on the logits after each pull (Section 3). A running average of past rewards serves as the baseline.

- `train_bandit(means, steps, lr, use_baseline, rng, noise=1.0)`: start from zero logits; at each step sample an arm, draw a reward from $N(\text{mean}, \text{noise}^2)$, update the logits by `lr * (r - b) * (onehot - pi)`, and update the baseline $b \leftarrow b + 0.05(r - b)$ when `use_baseline` (otherwise $b = 0$). Return the final probabilities.
- `best_arm_prob(probs, means)`.

The tests use five arms with means $5.0, 5.2, 5.4, 5.6, 6.0$ and unit noise: rewards are large and similar. With the baseline the policy puts more than 80 percent on the best arm after 3,000 pulls. e13 shows how much worse things get without a baseline when rewards sit even further from zero.

## Hints

1. Without a baseline every reward is about 5, so every update pushes the chosen arm up, the best and the worst alike; the baseline leaves only the differences, which are the signal.
2. Draw the arm with `rng.choice(K, p=pi)`.
3. The baseline is a function of the past only, never of the current action, so the update stays unbiased.
