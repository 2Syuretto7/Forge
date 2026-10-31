# Iterations against condition numbers from 10 to $10^5$

How does the cost of gradient descent grow with $\kappa$? Measure it in 1,000 dimensions where you can afford to run it, predict it where you cannot, and check that the two agree where both exist.

Gradient descent cares only about the eigenvalues (e06), so a diagonal matrix stands in for any quadratic with the same spectrum. Use eigenvalues spread log-uniformly from 1 to $\kappa$, the start $x_0 = \mathbf 1$, minimum at 0, and the best step $2/(1 + \kappa)$.

- `spectrum(kappa, d=1000)`: `np.geomspace(1, kappa, d)`.
- `run_iterations(kappa, eps=1e-6, d=1000)`: run gradient descent on the diagonal quadratic until the error norm falls below `eps` times its start, and return the count.
- `predict_iterations(kappa, eps=1e-6, d=1000)`: the same count without running: the error after $k$ steps is $\sqrt{\sum_i (1 - \eta\lambda_i)^{2k}}$, so find the smallest $k$ with that at most $\varepsilon\sqrt d$, by doubling $k$ and then bisecting.
- `slope(kappas, counts)`: the slope of $\log(\text{count})$ against $\log\kappa$, by least squares.

The tests run gradient descent for $\kappa$ up to 1,000, require the prediction to match it exactly there, then predict up to $10^5$ and find a slope near 1.

## Hints

1. The diagonal update is elementwise: `x -= step * lam * x`.
2. Work with logarithms of $\lvert 1 - \eta\lambda_i\rvert$ to keep the powers from underflowing: `np.exp(2 * k * np.log(np.abs(1 - step * lam)))`.
3. `np.polyfit(np.log(kappas), np.log(counts), 1)[0]`.
