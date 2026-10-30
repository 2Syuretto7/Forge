# A good first guess

Hardware square roots start Newton from a guess built out of the floating-point exponent: write $a = m \cdot 2^e$ with $m \in [0.5, 1)$ (`math.frexp`), and start from $\sqrt{m} \cdot 2^{e/2}$ approximated cheaply.

- `first_guess(a)`: with `m, e = math.frexp(a)`, return `(0.41 + 0.59 * m) * 2 ** (e // 2)`, times $\sqrt 2$ when `e` is odd. The linear part approximates $\sqrt m$ on $[0.5, 1)$ to within 2 percent.
- `iterations_to_full_precision(a, x0, tol=4e-16)`: Newton steps for $\sqrt a$ from `x0` until the relative error is below `tol`.

The tests check that from this guess every $a$ between $10^{-300}$ and $10^{300}$ needs at most 4 steps, while from $x_0 = a$ huge inputs need over 500.

## Hints

1. `math.frexp(a)` returns `(m, e)` with `a == m * 2**e`.
2. $\sqrt{m 2^e} = \sqrt m\, 2^{e/2}$; split off the odd power as $\sqrt 2$.
3. Each Newton step from a 2 percent error: $2 \times 10^{-2} \to 2 \times 10^{-4} \to 2 \times 10^{-8} \to 2 \times 10^{-16}$.
