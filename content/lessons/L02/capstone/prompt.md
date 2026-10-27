# Capstone: an A/B test analyzer that knows when to doubt itself

A product team runs an A/B test: variant A converts $k_A$ of $n_A$ visitors and variant B converts $k_B$ of $n_B$. Build an analyzer that answers "is B better?" two ways and explains when the two answers disagree.

Implement:

1. `bootstrap_diff(ka, na, kb, nb, B, seed)`: rebuild the 0/1 outcome arrays (ones first, then zeros), and resample each arm independently with replacement `B` times using one `np.random.default_rng(seed)` (arm A's index array of shape `(B, na)` first, then arm B's `(B, nb)`). Return the two arrays of resampled rates `(pa_star, pb_star)`.
2. `bayes_draws(ka, na, kb, nb, prior, draws, seed)`: with independent $\text{Beta}(a, b)$ priors given by `prior = (a, b)`, return `draws` posterior samples for each arm, A first then B, from one generator.
3. `analyze(ka, na, kb, nb)`: using `B=4000, seed=0` for the bootstrap and a uniform prior with `draws=100000, seed=0`, return a dict with:
   - `"diff"`: the observed $\hat p_B - \hat p_A$;
   - `"ci"`: the 95 percent percentile interval of the bootstrap differences;
   - `"prob_b_better"`: the posterior probability that $p_B > p_A$;
   - `"a_ci_boot"` and `"a_ci_bayes"`: 95 percent intervals for $p_A$ alone, from the bootstrap rates and from the posterior draws;
   - `"bootstrap_says"` and `"bayes_says"`: `"B"`, `"A"` or `"unclear"`. The bootstrap says `"B"` when the whole difference interval is strictly above 0 and `"A"` when strictly below; Bayes says `"B"` when the probability exceeds 0.95 and `"A"` when it is below 0.05.
4. `REPORT`: at least 100 words on when the two methods agree, when they disagree, and why. Run `analyze` on the four scenarios in the tests (a large clear effect, an arm with zero conversions, a small test, and a moderate test) and describe what you see. Mention the role of the prior and of small samples.
