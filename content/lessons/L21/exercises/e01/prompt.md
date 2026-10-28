# The policy gradient

For a policy $\pi_\theta = \operatorname{softmax}(\theta)$ over actions with rewards $r_a$, the gradient of the expected reward is
$$
\nabla_\theta\, \mathbb{E}_{a \sim \pi}[r_a] = \mathbb{E}_{a \sim \pi}\bigl[r_a\, \nabla_\theta \log \pi_\theta(a)\bigr],
$$
so it can be estimated from samples alone.

1. `score(theta, a)`: $\nabla_\theta \log \pi_\theta(a) = \text{onehot}(a) - p$, L07's $p - y$ with the sign flipped.
2. `exact_policy_gradient(theta, rewards)`: the expectation, by enumerating actions.
3. `reinforce_estimate(theta, rewards, n, seed, baseline=0.0)`: the average of $(r_a - b)\,\text{score}(a)$ over $n$ actions sampled with `np.random.default_rng(seed).choice(..., p=p)`.

## Hints

1. The identity follows from $\nabla \pi = \pi \nabla \log \pi$.
2. Subtracting a constant baseline leaves the estimate unbiased, because $\mathbb{E}[\text{score}] = 0$.
3. Sample all $n$ actions at once with `rng.choice(K, size=n, p=p)`.
