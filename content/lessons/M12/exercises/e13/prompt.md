# Diagnosing lost digits

- `conds(degree, n=200)`: for the monomial design matrix on $n$ points evenly spaced in $[0, 1]$, return `(cond_A, cond_AtA)` from `np.linalg.cond` (M14 explains how it is computed).
- `digits_kept(cond)`: about $16 - \log_{10}(\text{cond})$, clipped to $[0, 16]$.
- `better_basis(degree, n=200)`: the condition number of the design matrix when $x$ is first rescaled to $[-1, 1]$ and the columns are Chebyshev polynomials $T_0, T_1, \dots$ (`np.polynomial.chebyshev.chebvander`). Rescaling and a better basis remove most of the problem.

## Hints

1. `np.vander(x, degree + 1, increasing=True)`.
2. $\kappa(A^\top A)$ should come out close to $\kappa(A)^2$.
3. `2 * x - 1` maps $[0, 1]$ to $[-1, 1]$.
