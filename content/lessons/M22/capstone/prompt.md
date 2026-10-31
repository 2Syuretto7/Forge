# Capstone: a distribution library and the initialization scale

Part 1. Write eight samplers. Each takes its parameters, a sample `size` and a NumPy generator `rng`, and may use only `rng.random` (uniforms on $[0, 1)$):

1. `bernoulli(p, size, rng)` and `binomial(n, p, size, rng)`, the second by the inverse CDF: a table of cumulative probabilities and `np.searchsorted`.
2. `geometric(p, size, rng)`: the number of trials up to and including the first success, by the inverse CDF $\lfloor \log(1 - u)/\log(1 - p) \rfloor + 1$.
3. `poisson(lam, size, rng)`: by the inverse CDF, with the table long enough that the tail beyond it is below $10^{-15}$.
4. `uniform(a, b, size, rng)`, `exponential(lam, size, rng)`, `laplace(b, size, rng)` and `gaussian(mu, sigma, size, rng)`, the last by Box-Muller.

Discrete samplers return integer arrays. The tests draw $10^6$ samples from each and require the CDF distance of e11 below the DKW threshold at $\alpha = 0.001$.

Part 2. The leaky ReLU $f(y) = \max(y, a y)$ with slope $a \in [0, 1]$ generalizes ReLU ($a = 0$) and the identity ($a = 1$).

5. `leaky_second_moment(a)`: $\mathbb{E}[f(Z)^2]$ for a standard normal $Z$, derived by the symmetry argument of e15.
6. `init_std(fan_in, a)`: the weight standard deviation that keeps the second moment of activations constant through layers of width `fan_in` followed by $f$.
7. `depth_check(depth, width, a, multiplier=1.0, seed=0)`: e12's experiment with the leaky ReLU and weights of standard deviation `multiplier * init_std(width, a)`; return the list of second moments.

The tests require the average growth per layer, the 40th root of the last second moment, within 10 percent of 1 at the derived scale (as in e12, the final value itself wanders by a factor of a few at width 128), and the second moment to fall below $10^{-5}$ or rise above $10^5$ at 0.8 and 1.25 times it.
