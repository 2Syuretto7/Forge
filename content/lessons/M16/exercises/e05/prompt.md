# Critical points of polynomials

Polynomials are coefficient lists, lowest power first: `[c0, c1, c2]` is $c_0 + c_1 x + c_2 x^2$.

- `poly_eval(c, x)` by Horner's rule.
- `poly_deriv(c)`: the coefficients of the derivative.
- `critical_points(c)`: the real roots of the derivative, sorted (use `np.roots`, which wants the highest power first, and keep roots with imaginary part below `1e-9`).
- `classify(c, x)`: `"min"`, `"max"` or `"flat"` by the second-derivative test (flat when $|f''(x)| < 10^{-9}$).

The tests include a **gradient check**: `poly_deriv` agrees with central differences of `poly_eval`.

## Hints

1. The derivative of $c_k x^k$ is $k c_k x^{k-1}$.
2. `np.roots(d[::-1])`.
3. Apply `poly_deriv` twice for $f''$.
