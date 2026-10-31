# RL on arithmetic

A policy answers "$a + b \bmod 10$" for digits $a, b$ with logits $\theta[a, b, :]$ over the answer digit. Implement `rl_arithmetic(steps, lr, group, seed, beta=0.0, theta0=None)`: each step, for every one of the 100 prompts, sample `group` answers, reward 1 for the right digit, compute group advantages, and ascend $\sum \text{adv} \cdot \text{score} / \text{group}$; when `beta` is positive, also descend $\beta$ times the gradient of $\mathrm{KL}(\pi \,\|\, \pi_0)$, with $\pi_0$ the initial policy. Return the final logits and the accuracy of the greedy answers.

## Hints

1. The KL gradient with respect to the logits is $\pi \odot (\log(\pi/\pi_0) - \mathrm{KL})$.
2. Use one `np.random.default_rng(seed)` for the whole run.
3. From the uniform policy every prompt's group sometimes contains the right answer, so the signal is there from the first step; harder tasks need a policy that is already sometimes right, which is why RL follows fine-tuning.
