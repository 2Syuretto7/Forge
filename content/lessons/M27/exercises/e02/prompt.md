# Cross-entropy and KL divergence

Implement Section 3. All quantities in nats.

- `cross_entropy(p, q)`: $-\sum_x p(x)\log q(x)$, terms with $p(x) = 0$ contribute 0, and the result is `inf` if $q(x) = 0$ where $p(x) > 0$.
- `kl(p, q)`: $\sum_x p(x)\log\frac{p(x)}{q(x)}$ with the same conventions.

The tests check Gibbs' inequality on random pairs, the identity $H(p,q) = H(p) + \mathrm{KL}(p\|q)$, and the asymmetry example from the derivation.

## Hints

1. Restrict to `m = p > 0`.
2. If `np.any(q[m] == 0)`, return `float("inf")`.
3. `kl = cross_entropy(p, q) - entropy(p)` works, but computing it directly avoids cancellation when the two are close.
