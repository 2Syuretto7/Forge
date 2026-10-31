# The noise floor as a stationary distribution

On the quadratic $f(x) = \frac\mu2 x^2$ with stochastic gradients $\mu x + \sigma\xi/\sqrt B$, $\xi$ standard normal, constant-step SGD is $x_{k+1} = (1 - \eta\mu)x_k - \eta\sigma\xi_k/\sqrt B$: a Markov chain (M32) whose distribution settles to a Gaussian with mean 0 and variance

$$
v_\infty = \frac{\eta\sigma^2}{B\mu(2 - \eta\mu)} ,
$$

the fixed point of $v \leftarrow (1 - \eta\mu)^2 v + \eta^2\sigma^2/B$ (Section 3).

- `stationary_variance(eta, mu, sigma, B)`: the formula.
- `simulate(eta, mu, sigma, B, chains, steps, rng)`: run `chains` independent copies from $x = 0$ for `steps` steps, all at once as one array, and return the final values.

The tests compare the simulated variance with the formula over several steps and batch sizes.

## Hints

1. One vector update per step: `x = (1 - eta * mu) * x - eta * sigma * rng.standard_normal(chains) / np.sqrt(B)`.
2. The chain forgets its start at the rate $(1 - \eta\mu)^k$; run long enough that this is negligible.
3. Halving $\eta$ halves the variance, to first order; so does doubling $B$.
