# Polynomial regression

Fit polynomials by least squares on inputs in $[-1, 1]$.

- `design(x, degree)`: the `(n, degree + 1)` matrix with columns $1, x, x^2, \dots, x^{\text{degree}}$.
- `fit_poly(x, y, degree)`: coefficients by `np.linalg.lstsq` on the design matrix.
- `predict(coef, x)`.
- `mse(yhat, y)`.

## Hints

1. `np.vander(x, degree + 1, increasing=True)` builds the design matrix.
2. `lstsq(..., rcond=None)[0]`.
3. Keep inputs in $[-1, 1]$: powers of large numbers make the design badly conditioned.
