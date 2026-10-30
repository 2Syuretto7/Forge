# Orders of magnitude

On a ladder of powers of ten, every positive number sits between two rungs.

- `order_of_magnitude(x)` returns the integer `e` with `10**e <= abs(x) < 10**(e + 1)`.
- `nearest_power(x)` returns the integer `k` such that `10**k` is the nearest power of ten **on the log scale**: compare `log10(x)` with whole numbers. The switch from 1 to 10 happens at $\sqrt{10} \approx 3.162$, not at 5.5.
- `within_factor(a, b, k)` returns `True` when positive `a` and `b` are within a factor `k` of each other (in either direction).
- `ladder(values)` returns the values sorted from smallest to largest, each paired with its order of magnitude: `[(e, value), ...]`.

## Hints

1. Reuse the floor-of-log10 with the same rounding repair as in the previous exercise.
2. `round(math.log10(x))` rounds the log to the nearest whole number.
3. `sorted(values)` returns a new sorted list; build the pairs with a loop or a list comprehension.
