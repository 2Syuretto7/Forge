# Mutual information from a joint table

A joint distribution of two discrete variables is a 2-D array `P` with `P[x, y]` $= p(x, y)$, summing to 1. Implement Section 6.

- `marginals(P)` returns `(px, py)`.
- `conditional_entropy(P)`: $H(Y \mid X)$ in nats.
- `mutual_information(P)`: $I(X; Y)$ in nats, computed as $\sum p(x,y)\log\frac{p(x,y)}{p(x)p(y)}$.

The tests check the identities $I = H(Y) - H(Y\mid X)$ and $H(X,Y) = H(X) + H(Y\mid X)$, and the two extreme cases from the derivation.

## Hints

1. Marginals are row and column sums.
2. $H(Y\mid X) = -\sum p(x,y)\log\frac{p(x,y)}{p(x)}$, skipping zero cells.
3. Use the outer product `np.outer(px, py)` for the independence baseline.
