# Intervals: estimates with error bars

An honest estimate is an interval of positive numbers $[\text{lo}, \text{hi}]$. Write the class `Interval`:

- `Interval(lo, hi)` stores `self.lo` and `self.hi`; raise `ValueError` unless `0 < lo <= hi`.
- `a * b` multiplies two intervals (or an interval and a positive number). For positive numbers the smallest product is `lo * lo` and the largest `hi * hi`.
- `a / b` divides. The smallest quotient divides the smallest top by the **largest** bottom.
- `mid()` is the geometric midpoint $\sqrt{\text{lo} \cdot \text{hi}}$, the centre on a log scale.
- `factor()` is $\sqrt{\text{hi} / \text{lo}}$: the interval is `mid()` times or divided by `factor()`.
- `contains(x)` is true when `lo <= x <= hi`.

The tests check an **invariant**: for random intervals and random points inside them, every product and quotient of the points lies inside the product and quotient of the intervals.

## Hints

1. Turn a plain number `c` into the interval `Interval(c, c)` first, then use one formula.
2. `[a, b] / [c, d] = [a / d, b / c]`.
3. `math.sqrt` computes square roots.
