# Degree 1 to 20 on 10,000 points

- `exact_data(degree, n=10000)`: `x` evenly spaced on $[0, 1]$ and `y` the exact values of the polynomial with all coefficients equal to 1, $\sum_{k=0}^{\text{degree}} x^k$. Return `(x, y)`.
- `coef_errors(degree)`: fit that data at the same degree with the normal equations and with Householder QR (`np.linalg.qr`), and return `(err_normal, err_qr)`, the largest absolute coefficient error of each (the true coefficients are all 1).
- `sweep(max_degree=20)`: the list of `(degree, err_normal, err_qr)` for degrees 1 to `max_degree`.

Print the sweep: the normal equations lose digits steadily and are useless past about degree 10, while QR loses them about half as fast and still has five correct digits at degree 15.

## Hints

1. `np.vander(x, degree + 1, increasing=True)`.
2. `np.max(np.abs(c - 1))`.
3. For degrees above 12, `np.linalg.solve` on the normal equations may succeed and return nonsense; it does not always raise.
