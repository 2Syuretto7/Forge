# Improper integrals

- `to_infinity(f, a, tol=1e-10)`: $\int_a^\infty f$ by integrating over $[a, a + L]$ for $L = 1, 2, 4, \dots$ with your adaptive Simpson (provided), stopping when the extra piece $[a + L/2, a + L]$ contributes less than `tol` in absolute value.
- `square_root_singular(f, b)`: $\int_0^b f(x)\,dx$ for $f$ that blows up like $x^{-1/2}$ at 0, by substituting $x = t^2$: $\int_0^{\sqrt b} f(t^2)\,2t\,dt$, with adaptive Simpson; at $t = 0$ evaluate the new integrand at $10^{-12}$ instead.

## Hints

1. Sum the pieces as you go; each new piece is one adaptive call.
2. The substituted integrand $2t f(t^2)$ is smooth for $f(x) = x^{-1/2}g(x)$ with smooth $g$.
3. $\int_0^\infty e^{-x} = 1$, $\int_1^\infty x^{-2} = 1$ (slow tail: about $1/L$ remains, so many doublings), $\int_0^1 x^{-1/2} = 2$.
