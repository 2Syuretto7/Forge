# Capstone: a ReLU curve builder

The starter defines `TARGETS`: five curves, each with an interval and an error budget. Equal pieces would need more than 700 pieces in all (625 for the square root alone). Your drawings must use **120 pieces or fewer in total**.

Write:

- `max_gap(f, a, b, m=60)`: the largest gap between `f` and its chord from $(a, f(a))$ to $(b, f(b))$, at `m` equally spaced points of $[a, b]$.
- `adaptive_knots(f, a, b, tol)`: start with the single piece $[a, b]$; while some piece has `max_gap` above `tol`, split the piece with the largest gap at its midpoint. Return the sorted list of corners, ends included.
- `to_relus(f, knots)`: the description `(intercept, slope, inner_knots, weights)` of the piecewise-linear function through $(t, f(t))$ for these corners, as in the build movement (corners need not be equally spaced).
- `evaluate(desc, x)`: the value of the description at `x`.
- `build_all(targets)`: a dictionary from each target's name to its corners.

Then fill in `REPORT`: one sentence per curve saying how many pieces it needed and why (where the corners crowded). The tests check every drawing is within its budget at 4,001 test points, that the total is at most 120 pieces, and that the report gives each curve's count.
