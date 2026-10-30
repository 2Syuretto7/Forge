# Richardson extrapolation and Romberg integration

If a rule's error is $C h^p$ plus smaller terms, two results $T(h)$ and $T(h/2)$ cancel the leading error:

$$
R = \frac{2^p\,T(h/2) - T(h)}{2^p - 1} .
$$

- `richardson(t_h, t_h2, p)`: that combination.
- `romberg(f, a, b, levels)`: the trapezoid rule with $1, 2, 4, \dots, 2^{\text{levels}-1}$ strips, then repeated Richardson: the $k$-th column eliminates the $h^{2k}$ term, with $p = 2k$. Return the final (bottom-right) value.

One Richardson step on the trapezoid rule is exactly Simpson's rule; repeated, it reaches machine precision for smooth functions with a few dozen evaluations.

## Hints

1. Build the table row by row: `R[i][0]` is the trapezoid value with $2^i$ strips.
2. `R[i][k] = richardson(R[i-1][k-1], R[i][k-1], 2 * k)`.
3. Check: `richardson(trap(n), trap(2n), 2)` equals `simpson(2n)`.
