# Break it: a zero in the wrong place

Fit a categorical model to a small sample by maximum likelihood and some categories that the true distribution allows never appear. The model gives them probability 0, and

$$
\mathrm{KL}(p \,\|\, q) = \sum_x p(x)\log\frac{p(x)}{q(x)} = \infty
$$

as soon as $q(x) = 0$ for one $x$ with $p(x) > 0$: the first unseen event on held-out data costs infinitely many nats. The reverse divergence $\mathrm{KL}(q \,\|\, p)$ stays finite, because a zero in $q$ only drops a term.

- `kl(p, q)`: in nats, with $0\log 0 = 0$ and `inf` when $q(x) = 0 < p(x)$.
- `fit(samples, K, alpha=0.0)`: the add-$\alpha$ estimate $(\text{count}_x + \alpha)/(n + K\alpha)$ over categories $0, \dots, K-1$.
- `heldout_ce(q, test)`: the average of $-\log q(x)$ over the test samples, `inf` if any has probability 0.
- `best_alpha(train, test, K, alphas)`: the `alpha` with the lowest held-out cross-entropy.

## Hints

1. `np.bincount(samples, minlength=K)`.
2. Mask with `p > 0` before taking logarithms; check `q[p > 0] == 0` first.
3. Laplace's $\alpha = 1$ is a fine default; the tests let held-out data choose.
