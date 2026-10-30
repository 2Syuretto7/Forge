# Piecewise-linear curves from ReLUs

Section 6 wrote a piecewise-linear function as a straight line plus shifted ReLUs, one per interior corner.

- `hat(x)`: $\operatorname{relu}(x) - 2\operatorname{relu}(x - 1) + \operatorname{relu}(x - 2)$.
- `relu_sum(x, intercept, slope, knots, weights)`: $\text{intercept} + \text{slope} \cdot x + \sum_k w_k \operatorname{relu}(x - t_k)$.
- `interpolant(f, a, b, n)`: the description `(intercept, slope, knots, weights)` of the piecewise-linear function through the points $(t_j, f(t_j))$ at $n + 1$ equally spaced $t_0 = a, \dots, t_n = b$. The first piece is the line through the first two points (its intercept is its value at $x = 0$); each interior corner $t_1, \dots, t_{n-1}$ gets the weight "new slope minus old slope".

The tests check that your description reproduces the curve exactly at the corners, and that it is a straight line between them.

## Hints

1. Compute the slopes $s_j = (f(t_{j+1}) - f(t_j)) / (t_{j+1} - t_j)$ first.
2. The first line is $f(t_0) + s_0 (x - t_0)$, so its intercept is $f(t_0) - s_0 t_0$.
3. The weight at $t_j$ is $s_j - s_{j-1}$.
