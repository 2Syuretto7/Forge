# Break it: uncorrelated is not independent

For a **jointly** Gaussian pair, zero correlation means independence. For two variables that are each Gaussian, it does not. Take $x \sim N(0, 1)$ and an independent fair sign $s = \pm 1$, and set $y = sx$. Then $y$ is also $N(0, 1)$ and $\operatorname{Cov}(x, y) = \mathbb{E}[s]\,\mathbb{E}[x^2] = 0$, yet $\lvert y\rvert = \lvert x\rvert$ always.

- `sign_pair(n, rng)`: `n` pairs as two arrays, drawing `x = rng.standard_normal(n)` first and then the signs with `rng.random(n) < 0.5`.
- `correlation(x, y)`: the sample correlation.
- `square_correlation(x, y)`: the correlation of $x^2$ and $y^2$, which is 0 for independent variables.
- `zero_sum_fraction(x, y, tol=1e-12)`: the fraction of pairs with $\lvert x + y\rvert \le$ `tol`. For a jointly Gaussian pair, $x + y$ is Gaussian and this is 0.

## Hints

1. `np.corrcoef(x, y)[0, 1]`.
2. $x^2 = y^2$ exactly here, so their correlation is 1.
3. Half the time $s = -1$ and $x + y = 0$ exactly: the sum has an atom at 0, impossible for a Gaussian.
