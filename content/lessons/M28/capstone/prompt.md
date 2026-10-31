# Capstone: an optimization lab

Predict how many iterations gradient descent needs on a quadratic, then run it, on ten quadratics: five condition numbers, $\kappa \in \{10, 30, 100, 300, 1000\}$, each with two steps, $1/L$ and $2/(L + \mu)$.

1. `quadratic(eigs, seed)`: a symmetric matrix with eigenvalues `eigs` and random eigenvectors (the $Q$ of a QR decomposition, as in e06).
2. `gd_iterations(A, x0, step, eps=1e-6, max_iter=200000)`: iterations of gradient descent on $\frac12 x^\top A x$ (minimum at 0) until $\lVert x\rVert \le \varepsilon\lVert x_0\rVert$.
3. `predicted_iterations(A, x0, step, eps=1e-6)`: the same count from the eigendecomposition of $A$ alone: expand $x_0 = \sum_i c_i q_i$; after $k$ steps the error is $\sqrt{\sum_i c_i^2(1 - \eta\lambda_i)^{2k}}$; return the smallest $k$ at which it falls below $\varepsilon\lVert x_0\rVert$.
4. `rate_bound(eigs, step, eps=1e-6)`: $\lceil\log\varepsilon/\log\rho\rceil$ with $\rho = \max_i\lvert 1 - \eta\lambda_i\rvert$.
5. `lab(d=40, seed=0)`: for each $\kappa$ and step, eigenvalues `np.linspace(1, kappa, d)`, the matrix `quadratic(eigs, seed)`, the start $x_0$ from `np.random.default_rng(seed + 1).standard_normal(d)`; return a list of ten dicts with keys `"kappa"`, `"step"` (`"inverse_L"` or `"best"`), `"actual"`, `"predicted"` and `"bound"`.

The tests require every actual count within **15 percent** of the prediction, never above the rate bound, and the count for the best step to grow about tenfold from $\kappa = 100$ to $\kappa = 1000$.
