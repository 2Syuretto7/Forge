# Capstone: an adaptive quadrature library

The starter's `INTEGRALS` lists 20 problems as dictionaries with `"name"`, `"f"`, `"a"`, `"b"` (either may be infinite), `"singular"` (true when the integrand blows up at `a`) and `"exact"`.

1. `adaptive_simpson(f, a, b, tol)`: as in e03, returning `(value, evaluations)`.
2. `transformed(spec)`: a list of `(g, lo, hi)` pieces whose integrals add up to the spec's:
   - a finite, regular interval: `[(f, a, b)]`;
   - `singular`: substitute $x = a + t^2$, $g(t) = 2t\,f(a + t^2)$ on $[0, \sqrt{b - a}]$;
   - `b` infinite: substitute $x = a + \frac{t}{1 - t}$, $g(t) = f(x)/(1 - t)^2$ on $[0, 1]$;
   - both infinite: the two half-lines from 0, the left one as $f(-x)$ on $[0, \infty)$, each transformed as above.
   Where a transformed integrand cannot be evaluated at an end of its interval (a division by zero, an infinity or `nan`), evaluate it $10^{-12}$ inside instead.
3. `integrate(spec, tol=1e-10)`: sum adaptive Simpson over the pieces and return `(value, evaluations)`.
4. `report()`: for each integral, `(name, value, error, evaluations)`.

The tests require every error below $10^{-8}$ and the total number of evaluations below 300,000.
