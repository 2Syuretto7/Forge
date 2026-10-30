# How many pieces?

- `max_error(f, g, a, b, m=2001)`: the largest $|f(x) - g(x)|$ over `m` equally spaced points from $a$ to $b$.
- `pl_interp(f, a, b, n)`: the machine for the piecewise-linear interpolant of `f` on $n$ equal pieces (find the piece containing $x$ and interpolate between its ends; clamp $x$ to $[a, b]$).
- `pieces_needed(f, a, b, tol)`: the smallest $n$ whose interpolant is within `tol` of `f` everywhere (by `max_error`). Try $n = 1, 2, 3, \dots$

The tests confirm the puzzle: the hill $e^{-x^2}$ on $[-3, 3]$ needs 30 pieces for an error of 0.01.

## Hints

1. The piece index is `min(int((x - a) / h), n - 1)` with `h = (b - a) / n`.
2. Interpolate: `y0 + (y1 - y0) * (x - x0) / h`.
3. A `while` loop that increases `n` until the error is small enough.
