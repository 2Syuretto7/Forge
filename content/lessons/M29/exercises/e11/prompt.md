# Iteration counts against the condition number

Measure the iteration counts of gradient descent and heavy ball to reach a relative error of $10^{-8}$ on diagonal quadratics with eigenvalues `np.geomspace(1, kappa, 100)`, start $\mathbf 1$ and minimum 0, each with its optimal constants (e03).

- `count(method, kappa, eps=1e-8, max_iter=200000)`: iterations until the error norm falls below `eps` times its start.
- `loglog_slope(kappas, counts)`: the slope of $\log(\text{count})$ against $\log\kappa$.

The tests find a slope near 1 for gradient descent over $\kappa \in [10, 1000]$ and near $\frac12$ for heavy ball over $\kappa \in [10, 10^4]$: momentum turns $\kappa$ into $\sqrt\kappa$.

## Hints

1. The diagonal update is elementwise.
2. Heavy ball's optimal constants depend on $L = \kappa$ and $\mu = 1$.
3. `np.polyfit(np.log(kappas), np.log(counts), 1)[0]`.
