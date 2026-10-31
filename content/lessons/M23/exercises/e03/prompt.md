# The Gaussian log-density and its score

Evaluate the density of Section 3 for many points at once, stably, through the Cholesky factor $\Sigma = LL^\top$: with $z = L^{-1}(x - \mu)$,

$$
\log p(x) = -\tfrac12 \lVert z\rVert^2 - \sum_i \log L_{ii} - \tfrac d2 \log(2\pi) ,
$$

because $\sqrt{\det\Sigma} = \prod_i L_{ii}$.

- `logpdf(X, mu, Sigma)`: the log-density of each row of `X`, an array of length $n$.
- `score(X, mu, Sigma)`: the gradient of the log-density with respect to $x$, $-\Sigma^{-1}(x - \mu)$, one row per point.

The tests run a **gradient check** of `score` against differences of `logpdf`, and compare with the one-dimensional formula and with a product of one-dimensional densities when $\Sigma$ is diagonal. M37 will learn the score of data it cannot write down.

## Hints

1. `L = np.linalg.cholesky(Sigma)` and `Z = np.linalg.solve(L, (X - mu).T)`: each column is one $z$.
2. Never form $\Sigma^{-1}$ or $\det\Sigma$ explicitly; in 256 dimensions the determinant underflows.
3. `np.linalg.solve(Sigma, (X - mu).T).T` gives $\Sigma^{-1}(x - \mu)$ for every row.
