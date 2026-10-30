# Capstone: a curve-fitting service

The starter's `datasets()` returns six problems, each a dictionary with a name, the design matrix `X`, the observations `y` and the true coefficients `coef` (the data were generated from them, with a little noise or none).

1. `fit(X, y)`: least squares by Householder QR (`np.linalg.qr`) and a triangular solve.
2. `baseline(X, y)`: the normal equations.
3. `diagnostics(X, y, c)`: a dictionary with `"rmse"` (root mean squared residual), `"orth"` ($\max_j |x_j \cdot r| / (\|x_j\|\,\|y\|)$: how much of the residual still points along a column, relative to the size of the data; near 0 for a correct fit, even when the data fit exactly and the residual is pure rounding) and `"cond"` (the ratio of the largest to smallest absolute diagonal entry of $R$, a cheap estimate of $\kappa(X)$).
4. `report()`: for each dataset, a dictionary with `"name"`, `"err_qr"` and `"err_normal"` (largest absolute coefficient error of each method), and the diagnostics of the QR fit.

The tests require QR to recover every dataset's coefficients, and to beat the baseline by at least a factor of 100 on the two ill-conditioned datasets.
