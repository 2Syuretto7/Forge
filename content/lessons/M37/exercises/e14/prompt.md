# Break it: a score from a single noise level

A score model trained at only one noise level knows the right direction at that level and nowhere else (Section 6). Simulate the failure with exact scores: sample with the true time-dependent score, and with the score of time $t^* = 1$ used at every step.

- `frozen(score, t_star)`: a score function that ignores its time argument and always uses `t_star`.
- `reverse(score, n, T, steps, rng)`: e07's sampler on a geometric grid.
- `compare(score, data, t_star, rng)`: `(w1_true, w1_frozen)` for samples of the data's size, with $T = 4$ and 100 steps.

The tests find the frozen score's samples more than five times further from the data than the true score's: at $t = 1$ the noised mixture is a single broad hump, and its score cannot separate the components.

## Hints

1. `lambda x, t: score(x, t_star)`.
2. Look at a histogram of the frozen samples: where do they end up?
3. Real diffusion models condition the network on $t$ (or on the noise level) and train on all levels at once, weighting the loss so that none dominates.
