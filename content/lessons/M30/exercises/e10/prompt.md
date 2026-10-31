# An SVM on 50,000 points, stopped by the duality gap

Coordinate ascent loops over points one at a time, too slowly in the browser for 50,000 of them. **Accelerated projected gradient ascent** on the dual uses only two matrix-vector products per step: with $L = \lambda_{\max}(X^\top X)$, take $\alpha \leftarrow \operatorname{clip}(z + \nabla D(z)/L, 0, C)$ at a look-ahead point $z$ that adds momentum as in M29 (Nesterov's schedule $t_{k+1} = \frac{1 + \sqrt{1 + 4t_k^2}}{2}$, $z = \alpha_{k+1} + \frac{t_k - 1}{t_{k+1}}(\alpha_{k+1} - \alpha_k)$).

The starter's `make_data(n=50000, d=10, seed=0)` returns `(X, y)`.

- `train(X, y, C, tol=1e-4, max_iter=1500, check_every=25)`: run until the relative duality gap $(P(w) - D(\alpha))/P(w)$, checked every `check_every` steps, is at most `tol`; return `(alpha, w, gaps)` with the list of gaps checked.
- `relative_gap(alpha, X, y, C)`.

The tests train with $C = 0.01$ and require the gap below $10^{-4}$ and test accuracy above 0.9; and they check that the gap bounds the true suboptimality from above, against a much longer run.

## Hints

1. $\nabla D(z) = 1 - y \odot X(X^\top(z \odot y))$.
2. $P(w)$ is e05's objective with $w = X^\top(\alpha\odot y)$.
3. `np.linalg.eigvalsh(X.T @ X)[-1]`: a 10 by 10 matrix.
