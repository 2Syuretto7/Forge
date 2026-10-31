# Break it: a bad local minimum

Convexity is what makes "the gradient is zero" mean "the problem is solved". Without it, gradient descent finds whichever minimum the start drains into. Take the tilted double well

$$
f(x) = (x^2 - 1)^2 + 0.3x ,
$$

whose global minimum is near $x = -1.04$ and whose other minimum, near $x = 0.96$, is higher.

- `f(x)` and `fprime(x)`.
- `descend(x0, step=0.01, iters=5000)`: gradient descent in one dimension; return the final point.
- `basin_fraction(starts)`: the fraction of starting points from which descent reaches the global minimum (final point below 0).
- `minima()`: the two local minima, found by bisection on `fprime` over $[-2, -0.5]$ and $[0.5, 2]$, as a sorted pair.

The tests check that about 48 percent of starts uniform on $[-2, 2]$ end in the worse minimum, and that a second-derivative check, $f'' > 0$ at both points, cannot tell a local minimum from the global one.

## Hints

1. $f'(x) = 4x(x^2 - 1) + 0.3$.
2. The boundary between the two basins is the local maximum between them, near $x = 0.075$.
3. Convex problems have a single basin: every start ends at the same minimum value.
