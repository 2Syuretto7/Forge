# The logarithm by inverting the exponential

The starter provides `exp(x)` from the previous exercise.

- `ln(y)`: the natural logarithm of $y > 0$, by bisection on `exp`. Find a bracket first: the answer lies between $-750$ and $750$ for every positive float. Halve 100 times. Raise `ValueError` for $y \leq 0$.
- `log_base(y, b)`: $\log_b y = \ln y / \ln b$.
- `digits(n)`: the number of decimal digits of a positive integer $n$, from `log_base(n, 10)`: the floor plus one. Floating point can land a hair below an exact power of ten, so check the answer against `10 ** (d - 1) <= n < 10 ** d` and adjust.

The tests check an **invariant**: $\ln(xy) = \ln x + \ln y$ for many random $x$, $y$.

## Hints

1. Bisection keeps the half where `exp(mid) < y` decides the direction, exactly as M04.
2. `ln(y) / ln(b)`.
3. `d = math.floor(log_base(n, 10)) + 1`, then fix by one step if needed.
