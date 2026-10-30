# Inverse by bisection

For an increasing function, you can run the machine backwards without a formula.

- `inverse(f, y, lo, hi, steps=60)`: find $x$ in $[\text{lo}, \text{hi}]$ with $f(x) = y$, assuming $f$ is increasing and $f(\text{lo}) \leq y \leq f(\text{hi})$; raise `ValueError` if $y$ is not bracketed. Repeat `steps` times: take the midpoint, and keep the half that still brackets $y$. Return the final midpoint.
- `make_inverse(f, lo, hi)`: return the machine $y \mapsto$ `inverse(f, y, lo, hi)`.

The tests check an **invariant**: for several increasing functions and many random inputs, `f(inverse(f, f(x)))` is `f(x)` and `inverse(f, f(x))` is `x`, to within `1e-9`.

## Hints

1. `if not f(lo) <= y <= f(hi): raise ValueError(...)`.
2. `mid = (lo + hi) / 2`; if `f(mid) < y`, the answer is in `[mid, hi]`.
3. Sixty halvings shrink any reasonable interval below rounding level.
