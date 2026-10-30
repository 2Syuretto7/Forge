# Gradients in 10,000 dimensions

$f(x) = \sum_i \log(1 + e^{x_i}) + \frac12\sum_i (x_{i+1} - x_i)^2$, a smooth function of $n$ inputs.

- `f(x)`: vectorized, $O(n)$.
- `grad(x)`: the analytic gradient, also $O(n)$: the softplus derivative is the sigmoid, and the chain term gives $(x_i - x_{i-1}) - (x_{i+1} - x_i)$ inside, with one-sided terms at the ends.
- `fd_grad(x, h=1e-6)`: central differences, $2n$ calls of `f`.
- `speedup(n)`: the time of `fd_grad` divided by the time of `grad` at a random point of length `n`.

The tests run a **gradient check** at $n = 2000$ and measure a speedup in the hundreds or more.

## Hints

1. `np.logaddexp(0, x)` computes $\log(1 + e^x)$ without overflow.
2. With `d = np.diff(x)`, the gradient of the second term is `np.concatenate([[0], d]) - np.concatenate([d, [0]])`.
3. `time.perf_counter` around each call.
