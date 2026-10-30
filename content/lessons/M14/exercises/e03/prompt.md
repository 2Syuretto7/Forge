# The ellipse of a 2 by 2 matrix

- `singular_values_2x2(A)`: $\sigma_1 \geq \sigma_2$ from the eigenvalues of $A^\top A$ (closed form for a symmetric 2 by 2 matrix).
- `circle_image_extremes(A, n=3600)`: map $n$ evenly spaced points of the unit circle and return the largest and smallest lengths of the images.
- `area_factor(A)`: $|\det A|$.

The tests check an **invariant** on random matrices: the extremes of the image equal $\sigma_1$ and $\sigma_2$ (to the sampling accuracy), and $\sigma_1 \sigma_2 = |\det A|$.

## Hints

1. For $\begin{pmatrix} p & q \\ q & r \end{pmatrix}$ the eigenvalues are $\frac{p + r}{2} \pm \sqrt{\left(\frac{p - r}{2}\right)^2 + q^2}$.
2. `t = np.linspace(0, 2 * np.pi, n, endpoint=False)`.
3. Clip a tiny negative eigenvalue to 0 before the square root.
