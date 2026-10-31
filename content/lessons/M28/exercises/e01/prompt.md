# Testing convexity by chords

A function is convex when every chord lies on or above the graph: $f(ta + (1 - t)b) \le t f(a) + (1 - t)f(b)$ for all $a, b$ and $t \in [0, 1]$ (Section 1). A test cannot check every chord, but it can look hard for a violation.

- `chord_violation(f, a, b, ts)`: the largest value of $f(ta + (1 - t)b) - [t f(a) + (1 - t)f(b)]$ over the weights `ts`; positive means a violation. `a` and `b` may be vectors and `f` takes one point.
- `search_violation(f, dim, trials, rng, scale=3.0)`: draw `trials` random pairs of points with coordinates uniform in $[-\text{scale}, \text{scale}]$ and return the largest violation found, with `ts = np.linspace(0, 1, 21)`.
- `second_difference_min(f, lo, hi, n=2001)`: for a function of one variable, the smallest $f(x - h) - 2f(x) + f(x + h)$ over a grid of spacing $h$; a convex function has none negative (up to rounding).

The tests find no violation for $x^2$, $\lvert x\rvert$, $e^x$, log-sum-exp and a norm, and find violations for $\sin x$, $x^3$ and the product $xy$.

## Hints

1. `ts` may include 0 and 1, where the violation is exactly 0.
2. Points: `rng.uniform(-scale, scale, size=dim)`.
3. Rounding can make a convex function's second differences slightly negative; compare against a small tolerance.
