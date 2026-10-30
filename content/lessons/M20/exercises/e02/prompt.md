# Monte Carlo in the plane

- `mc_integral(f, box, n, seed=0)`: for `box = (ax, bx, ay, by)`, draw `n` uniform points with `np.random.default_rng(seed)`, and return `(estimate, standard_error)`: the area of the box times the mean of $f$, and the area times the sample standard deviation over $\sqrt n$.
- `disc_area(n, seed=0)`: the area of the unit disc as the integral of the indicator $x^2 + y^2 \leq 1$ over $[-1, 1]^2$.

The error shrinks like $1/\sqrt n$ in any dimension, slowly but without the curse that a grid suffers (Movement 4).

## Hints

1. `x = rng.uniform(ax, bx, n)`, the same for `y`.
2. `np.std(v, ddof=1) / np.sqrt(n)`.
3. The tests allow 4 standard errors.
