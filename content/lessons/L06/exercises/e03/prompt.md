# Measuring bias and variance by simulation

Section 2's decomposition is an identity about averages over training sets. Measure it.

`bias_variance(degree, n, sigma, x0, trials, seed)`: for `trials` independent training sets, each drawn as `x = rng.uniform(-1, 1, n)`, `y = sin(pi x) + sigma * rng.normal(size=n)` from one `np.random.default_rng(seed)` (x first, then y, per trial), fit a polynomial of the given degree and record its prediction at the point `x0`. Return a dict with:

- `"bias2"`: $(f(x_0) - \overline{\hat f}(x_0))^2$,
- `"variance"`: the variance of the predictions (divide by `trials`),
- `"noise"`: $\sigma^2$,
- `"expected_error"`: the average of $(y_0 - \hat f(x_0))^2$ where for each trial a fresh test target $y_0 = f(x_0) + \sigma\epsilon$ is drawn after that trial's training data.

The test checks that `bias2 + variance + noise` matches `expected_error` within Monte Carlo error, and that bias falls and variance rises with degree.

## Hints

1. Use one generator for everything, in the order x, y, then the test noise, per trial.
2. `np.var(preds)` divides by `trials`.
3. Use at least a few thousand trials for stable averages.
