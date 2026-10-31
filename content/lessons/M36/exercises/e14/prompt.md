# Break it: a baseline that peeks at the action

The baseline proof needed $b$ to be independent of the sampled action: then $\mathbb{E}[b\,(e_a - \pi)] = b\,\mathbb{E}[e_a - \pi] = 0$ (Section 3). Let the baseline depend on $a$ and the expectation no longer vanishes: the estimator becomes biased, and can point the wrong way.

- `estimates(z, r, n, rng, baseline_fn)`: single-sample estimates $(r_a - b(a))(e_a - \pi)$ with `baseline_fn(a)` evaluated at each sampled action.
- `bias(z, r, baseline_fn, n, rng)`: the largest absolute difference between the mean of the estimates and the exact gradient $\pi\odot(r - \pi\cdot r)$.

The tests find a constant baseline unbiased, the baseline $b(a) = 0.5\,r_a$ halving the gradient, and $b(a) = r_a$ wiping it out entirely.

## Hints

1. With $b(a) = cr_a$ every estimate is $(1 - c)r_a(e_a - \pi)$: the expectation is $(1 - c)$ times the true gradient.
2. Action-dependent baselines exist in the literature, but they come with a correction term that restores unbiasedness.
3. The advantage $Q(s, a) - V(s)$ depends on the action through $Q$, not through the baseline $V$; that is why it is safe.
