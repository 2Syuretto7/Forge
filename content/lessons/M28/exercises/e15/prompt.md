# Break it: a convex function of a convex function

Sums, maxima and nonnegative multiples of convex functions are convex, and so is a convex function of an affine map. A convex function of a convex function is convex only if the outer function is also **nondecreasing** (Section 1). Composition rules decide quickly whether a loss is convex; misapplied, they mislead.

- `compose(g, h)`: the function $x \mapsto g(h(x))$.
- `second_difference_min(f, lo, hi, n=4001)`: as in e01.
- `is_nondecreasing(g, lo, hi, n=4001)`: whether $g$ never decreases on a grid.

The tests check three compositions on $[-2, 2]$: $e^{x^2}$ (outer convex and increasing: convex), $(x^2 - 1)^2$ (outer $u^2$ convex but decreasing for $u < 0$: not convex), and $\log(1 + e^{x})$ composed with an affine map (convex).

## Hints

1. `lambda x: g(h(x))`.
2. For $(x^2 - 1)^2$, the inner $h = x^2 - 1$ takes negative values on $(-1, 1)$, where $u^2$ decreases.
3. Check the outer function only on the range the inner one actually takes.
