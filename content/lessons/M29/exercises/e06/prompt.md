# Stochastic gradient descent and its noise floor

Least squares on $n$ rows has gradient $\frac1n X^\top(Xw - y)$. **Stochastic gradient descent** replaces it by the same formula on a random minibatch of $B$ rows: unbiased, but noisy (Section 3). With a constant step the iterates never settle; they wander in a cloud around the optimum whose size is proportional to the step.

- `sgd(X, y, w0, step, iters, batch, rng)`: minibatches drawn with `rng.integers(0, n, size=batch)` each step; return the final iterate and the list of full losses $\frac{1}{2n}\lVert Xw - y\rVert^2$ every 10 steps.
- `excess_floor(X, y, step, batch, rng, iters=4000)`: the average excess loss $f(w) - f(w^\star)$ over the second half of a run started at $w^\star$.

The tests show the floor halving when the step halves, and shrinking when the batch grows.

## Hints

1. Minibatch gradient: `Xb.T @ (Xb @ w - yb) / batch`.
2. $w^\star$ from `np.linalg.lstsq`.
3. Starting at the optimum isolates the noise: any excess is the cloud's size.
