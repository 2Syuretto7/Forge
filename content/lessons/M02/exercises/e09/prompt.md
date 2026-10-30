# Complete the square

Every quadratic can be written as a shifted, scaled square plus a constant:

$$
a x^2 + b x + c = a (x + h)^2 + k .
$$

- `complete_square(a, b, c)` returns `(h, k)`. Expand the right side and match the coefficients of $x$ and of the constant.
- `vertex(a, b, c)` returns the point `(x, y)` where the parabola $y = ax^2 + bx + c$ turns: the square is zero there.
- `minimum_value(a, b, c)` returns the smallest value of $ax^2 + bx + c$ when $a > 0$, and raises `ValueError` otherwise (a downward parabola has no minimum).

## Hints

1. $a(x + h)^2 + k = a x^2 + 2ah\,x + ah^2 + k$, so $2ah = b$ and $ah^2 + k = c$.
2. $h = \dfrac{b}{2a}$ and $k = c - \dfrac{b^2}{4a}$.
3. The vertex is at $x = -h$, where the value is $k$.
