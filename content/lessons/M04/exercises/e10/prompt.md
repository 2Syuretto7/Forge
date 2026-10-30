# A thousand points, many pieces

Use NumPy to measure the $1/n^2$ law at scale.

- `interp_error(f, a, b, n, m=1000)`: build the $n$-piece interpolant with `np.interp(x, knots, f(knots))` (it does exactly the piecewise-linear interpolation of the build movement) and return its largest error at `m` random points of $[a, b]$ drawn with `np.random.default_rng(0).uniform(a, b, m)`. Here `f` takes and returns NumPy arrays.
- `error_table(f, a, b, ns)`: the list of `interp_error` values for each $n$ in `ns`.
- `shrink_factors(errors)`: the ratios `errors[i] / errors[i + 1]`.

## Hints

1. `knots = np.linspace(a, b, n + 1)`.
2. `np.max(np.abs(f(x) - np.interp(x, knots, f(knots))))`.
3. A list comprehension over consecutive pairs.
