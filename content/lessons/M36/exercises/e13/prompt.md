# Break it: rewards far from zero, no baseline

REINFORCE is unbiased with or without a baseline, but its noise grows with the size of the rewards, not with their differences (Section 3). Add 100 to every reward of a bandit and the estimates' variance grows by orders of magnitude; learning slows to a crawl although the best arm is exactly as much better as before.

- `gradient_variance(z, r, n, rng, b=0.0)`: the total variance of $n$ single-sample estimates $(r_a - b)(e_a - \pi)$.
- `train(means, offset, steps, lr, use_baseline, rng)`: REINFORCE on a deterministic bandit with rewards `means + offset`, a running-average baseline $b \leftarrow b + 0.05(r - b)$ when requested, started at the first reward, and return the final probability of the best arm.

The tests find the variance with offset 100 more than a thousand times that with offset 0, the baseline removing the difference, and training with the offset and no baseline failing to find the best arm while the same training with a baseline succeeds.

## Hints

1. $\operatorname{Var}[(r_a - b)(e_a - \pi)]$ contains $(\bar r - b)^2\,\mathbb{E}\lVert e_a - \pi\rVert^2$: an offset enters squared.
2. A learning rate small enough to survive the noise of rewards near 100 is far too small for the signal, which is a difference of order 1.
3. Normalizing rewards (subtracting a running mean and dividing by a running standard deviation) is the practical form of the same fix.
