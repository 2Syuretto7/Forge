# The line fit as two equations

For a straight line $y \approx w_0 + w_1 x$, the normal equations are M02's two equations in two unknowns:

$$
\begin{pmatrix} n & \sum x_i \\ \sum x_i & \sum x_i^2 \end{pmatrix} \begin{pmatrix} w_0 \\ w_1 \end{pmatrix} = \begin{pmatrix} \sum y_i \\ \sum x_i y_i \end{pmatrix} .
$$

- `line_fit(x, y)`: solve them with M02's formula, $w = \frac{1}{ad - bc}(\dots)$, and return `(w0, w1)`.
- `centered_fit(x, y)`: the same line from means: $w_1 = \sum (x_i - \bar x)(y_i - \bar y) / \sum (x_i - \bar x)^2$ and $w_0 = \bar y - w_1 \bar x$.
- `residual_checks(x, y, w0, w1)`: `(sum of residuals, sum of x times residuals)`.

## Hints

1. With $a, b, c, d$ the entries and $p, q$ the right side: $w_0 = (pd - bq)/(ad - bc)$ and $w_1 = (aq - cp)/(ad - bc)$.
2. `x.mean()` and `y.mean()`.
3. At the least-squares line both checks are zero up to rounding.
