# Too few points per wiggle

$\int_0^1 \sin(200x)\,dx = \frac{1 - \cos 200}{200}$.

- `simpson_error(n)`: the error of Simpson's rule with `n` strips.
- `points_per_period(n, freq=200, length=1.0)`: the number of sample points in one period $2\pi/\text{freq}$ of the oscillation.
- `first_good_n(tol=1e-8)`: the smallest power of two $n \geq 2$ for which `simpson_error(n) < tol`.

Below about two points per period the samples cannot even tell the function oscillates (aliasing); below about ten, Simpson's error formula is meaningless. Good accuracy needs many points per period: here $n$ in the thousands.

## Hints

1. Simpson as in e02.
2. A period contains $\frac{2\pi}{\text{freq}} \cdot \frac{n}{\text{length}}$ strips.
3. Loop over $n = 2, 4, 8, \dots$
