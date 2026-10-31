# REINFORCE for a softmax policy

A policy over $K$ actions with logits $z$ chooses action $a$ with probability $\pi_a = \mathrm{softmax}(z)_a$ and receives reward $r_a$. The gradient of $J = \sum_a\pi_ar_a$ in $z$ is $\pi\odot(r - \pi\cdot r)$, and the log-derivative trick gives the unbiased **REINFORCE** estimator (Section 2)

$$
\hat g = r_a\,\nabla_z\log\pi_a = r_a\,(e_a - \pi), \qquad a \sim \pi .
$$

- `softmax(z)` and `log_softmax(z)`.
- `score(a, z)`: $e_a - \pi$, the gradient of $\log\pi_a$.
- `exact_grad(z, r)`.
- `reinforce(z, r, n, rng)`: the average of $n$ single-sample estimates.

The tests run a **gradient check** of the score against finite differences of `log_softmax`, and confirm that 100,000 samples recover the exact gradient.

## Hints

1. `log_softmax(z) = z - max(z) - log(sum(exp(z - max(z))))`.
2. Sample all $n$ actions at once with `rng.choice(K, size=n, p=pi)`, then average `r[a] * (onehot(a) - pi)`.
3. The scores average to zero under the policy: $\mathbb{E}[e_a - \pi] = 0$. That fact is what makes baselines possible.
