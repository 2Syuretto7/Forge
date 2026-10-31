# Baselines

Subtracting any constant $b$ from the reward leaves REINFORCE unbiased, because the score has mean zero: $\mathbb{E}[(r_a - b)(e_a - \pi)] = \mathbb{E}[r_a(e_a - \pi)]$. It changes the variance, often dramatically (Section 3). A natural choice is $b = \mathbb{E}r_a$, the policy's average reward; the variance-minimizing constant weights rewards by the squared score.

- `estimates(z, r, n, rng, b=0.0)`: an array of shape `(n, K)` of single-sample estimates $(r_a - b)(e_a - \pi)$.
- `total_variance(G)`: the sum over components of the sample variances of the estimates.
- `optimal_baseline(z, r)`: $b^* = \frac{\mathbb{E}[r_a\lVert e_a - \pi\rVert^2]}{\mathbb{E}[\lVert e_a - \pi\rVert^2]}$, computed exactly from $\pi$.

The tests add a constant 10 to every reward: without a baseline the variance rises more than fortyfold, with $b = \mathbb{E}r$ it does not change, and the mean of the estimates stays the exact gradient throughout.

## Hints

1. The baseline does not depend on the sampled action, so it can be pulled out of the expectation, where it multiplies $\mathbb{E}[e_a - \pi] = 0$.
2. $\lVert e_a - \pi\rVert^2 = 1 - 2\pi_a + \lVert\pi\rVert^2$.
3. Shifting all rewards by a constant does not change which action is best, but without a baseline it changes the noise of every estimate.
