# Induction, checked for every n at once

A polynomial is a list of exact coefficients `[c0, c1, c2, ...]` meaning $c_0 + c_1 n + c_2 n^2 + \dots$ (use `Fraction` coefficients so $n(n+1)/2$ is exact). A claim "$\sum_{k=1}^{n} f(k) = F(n)$ for every $n \geq 1$" is proved by induction from:

- **base:** $F(1) = f(1)$;
- **step:** $F(n + 1) - F(n) = f(n + 1)$ **as polynomials**: the coefficient lists agree, so the equation holds for every $n$ at once.

Write the polynomial helpers and the checker:

- `peval(p, n)`: the value at `n` (Horner's rule).
- `padd(p, q)` and `pscale(p, c)`: sum, and multiple by a number.
- `pmul(p, q)`: product.
- `pshift(p)`: the polynomial $p(n + 1)$. Expand $(n + 1)^j$ with binomial coefficients, or build it from `pmul` by powers of `[1, 1]`.
- `pequal(p, q)`: equal after removing trailing zero coefficients.
- `induction_check(f, F)`: the pair `(base_ok, step_ok)`.

The tests prove $\sum k^2 = \frac{n(n+1)(2n+1)}{6}$ and reject a formula that fits the first case but not the step.

## Hints

1. `pshift(p) = sum over j of c_j * (n + 1)^j`, and `(n + 1)^j` is `pmul` of `[1, 1]` with itself `j` times.
2. The step compares `padd(pshift(F), pscale(F, -1))` with `pshift(f)`.
3. Trim with `while p and p[-1] == 0: p = p[:-1]`.
