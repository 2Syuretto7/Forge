# Every input for an output

Bisection finds one input and needs a bracket. For a function that is not one-to-one, first find every bracket.

- `brackets(f, y, lo, hi, m=1000)`: split $[\text{lo}, \text{hi}]$ into `m` equal cells and return the list of cells `(a, b)` on which $f - y$ changes sign or hits zero at an end. Count a grid point where $f = y$ exactly once.
- `bisect(f, y, a, b, steps=60)`: bisection for a root of $f - y$ on a cell whose ends have opposite signs (or a zero), not assuming $f$ is increasing.
- `all_preimages(f, y, lo, hi)`: every solution of $f(x) = y$ in the interval, sorted, one per bracket.

## Hints

1. With `g = lambda x: f(x) - y`, a cell brackets a root when `g(a) == 0` or `g(a) * g(b) < 0`.
2. In `bisect`, keep the half whose ends still have opposite signs.
3. The tests use $x^2 = 4$ on $[-3, 3]$ and $\sin x = 0.5$ on $[0, 10]$.
