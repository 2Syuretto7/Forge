# Integrating in polar coordinates

`integrate_polar(g, R, n=400)`: $\int_0^{2\pi}\!\int_0^R g(r\cos\theta, r\sin\theta)\,r\,dr\,d\theta$ with the midpoint rule on an $n \times n$ grid in $(r, \theta)$, for a vectorized `g(x, y)`.

The tests compute the area of the disc, $\iint e^{-(x^2 + y^2)} = \pi$ over the whole plane (with $R = 6$), and $\iint_{\text{disc}} (x^2 + y^2) = \pi/2$; each would need a much finer Cartesian grid, because the disc's round edge cuts through square cells.

## Hints

1. Midpoints in $r$ and $\theta$, a mesh, and the factor $r$ inside the sum.
2. The cell area in $(r, \theta)$ is $\frac{R}{n}\cdot\frac{2\pi}{n}$.
3. Forgetting the factor $r$ gives $2\pi R$ for the "area" of the disc, a length.
