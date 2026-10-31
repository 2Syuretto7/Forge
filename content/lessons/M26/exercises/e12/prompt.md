# Condition numbers from 10 to $10^{16}$

The **condition number** of a problem bounds how much it can amplify relative errors in its input (Section 4). A backward-stable algorithm, such as Gaussian elimination with partial pivoting, then delivers a relative error of about $\kappa\,\varepsilon$: it loses about $\log_{10}\kappa$ digits, and no algorithm can do much better.

- `scalar_condition(f, df, x)`: $\lvert x f'(x)/f(x)\rvert$.
- `hilbert(n)`: the matrix with entries $1/(i + j + 1)$, $i, j = 0, \dots, n - 1$, a famously ill-conditioned matrix.
- `matrix_condition(A)`: $\sigma_{\max}/\sigma_{\min}$ from `np.linalg.svd(A, compute_uv=False)`.
- `solve_error(n)`: solve $H_n x = H_n\mathbf 1$ with `np.linalg.solve` and return the relative error of $x$ against $\mathbf 1$ (in the 2-norm) together with $\kappa(H_n)$.

The tests check that the error tracks $\kappa\varepsilon$ from $n = 2$ to $n = 12$.

## Hints

1. `np.add.outer(np.arange(n), np.arange(n))` gives $i + j$.
2. $\kappa$ of $\log$ at $x$ is $1/\lvert\log x\rvert$: huge near $x = 1$.
3. Beyond $\kappa \approx 10^{16}$ the computed $\sigma_{\min}$ is itself rounding noise, and the computed condition number stops meaning anything.
