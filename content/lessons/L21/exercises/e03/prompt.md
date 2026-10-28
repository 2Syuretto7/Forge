# REINFORCE on a bandit

Implement `train_bandit(means, steps, lr, seed, batch=16)`: arm $a$ pays `means[a]` plus standard normal noise. Each step, sample `batch` arms from $\operatorname{softmax}(\theta)$ (with one `np.random.default_rng(seed)` for the whole run), use the batch's mean reward as the baseline, and add `lr` times the average of $(r - b)(\text{onehot}(a) - p)$ to $\theta$. Return the final probabilities.

## Hints

1. Draw the arms and the noise from the same generator, arms first.
2. The baseline is the mean of this batch's rewards.
3. The policy should end up on the best arm even though every reward is noisy.
