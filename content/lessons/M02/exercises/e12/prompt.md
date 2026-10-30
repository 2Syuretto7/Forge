# Many points, two unknowns

A line $y = m x + c$ has two unknowns. Two points pin it down; fifty noisy points do not lie on any one line.

- `line_through(p1, p2)`: the slope and intercept `(m, c)` of the line through two points `(x, y)` with different `x`. This is a two-by-two system; solve it however you like.
- `misfit(points, m, c)`: the sum over all points of the squared vertical miss $(y_i - (m x_i + c))^2$.
- `best_pair_line(points)`: try the line through every pair of points (with different `x`) and return the `(m, c)` with the smallest misfit on all the points.

The tests generate fifty points near a line. Compare your best pair's misfit with the misfit of the true line used to generate them. Pairs do well, but there is a better line than any pair gives: that is the puzzle of M12.

## Hints

1. $m = (y_2 - y_1)/(x_2 - x_1)$ and $c = y_1 - m x_1$.
2. `sum((y - (m * x + c)) ** 2 for x, y in points)`.
3. Two nested loops over indices `i < j`.
