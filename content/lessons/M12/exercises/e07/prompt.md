# Polynomial fitting

- `design(x, degree)`: the matrix with columns $1, x, x^2, \dots, x^{\text{degree}}$.
- `polyfit_ls(x, y, degree)`: the coefficients, lowest power first, by least squares through `np.linalg.qr`.
- `polyval(c, x)`: evaluate $\sum_k c_k x^k$ by Horner's rule (M05).

## Hints

1. `np.vander(x, degree + 1, increasing=True)`, or stack the powers yourself.
2. Reuse the QR solve of e05.
3. Horner: start from the highest coefficient, `s = s * x + c[k]`.
