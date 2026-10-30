# One equals two

The "proof" in the break-it movement, line by line, for $a = b$:

| line | claim |
| --- | --- |
| 0 | $a = b$ |
| 1 | $a^2 = ab$ |
| 2 | $a^2 - b^2 = ab - b^2$ |
| 3 | $(a + b)(a - b) = b(a - b)$ |
| 4 | $a + b = b$ |
| 5 | $2b = b$ |
| 6 | $2 = 1$ |

The starter encodes each line as a pair of functions `(left, right)` of `(a, b)`, in `LINES`. Write:

- `holds(line, a, b)`: whether the line's two sides are equal at that `(a, b)`.
- `first_false_line(lines, a, b)`: the index of the first line that is false at `(a, b)`.
- `divisor_at_step(a, b)`: the value of what line 4 divided both sides of line 3 by, $a - b$, at the given point.

Run them at $a = b = 1$. The first false line follows directly from a division by the value you just computed.

## Hints

1. `left(a, b) == right(a, b)`.
2. Loop over `enumerate(lines)`.
3. Line 4 cancels the common factor $(a - b)$.
