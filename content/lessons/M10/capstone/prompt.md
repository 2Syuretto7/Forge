# Capstone: transform studio

The starter defines `F`, a letter F drawn as 10 vertices, and `TARGETS`, eight entries of the form `(description, points)`, where `points` is the F after an unknown 2 by 2 linear map.

1. Implement the primitives `rot(degrees)`, `scale(sx, sy)`, `shear_x(k)` (the map $(x, y) \mapsto (x + ky, y)$) and `reflect_x()` (across the $x$ axis), and `swap()` (across the line $y = x$).
2. `recipes()`: for each target, a list of primitive matrices **in the order applied**, read off the description. Derive each one by hand: write down where $(1, 0)$ and $(0, 1)$ go.
3. `build(steps)`: the single matrix of the recipe.
4. `fit_matrix(src, dst)`: the 2 by 2 matrix $M$ that best maps the rows of `src` to the rows of `dst` in least squares, from `np.linalg.lstsq`; an independent numerical check.
5. `report()`: for each target, a tuple `(max error of your recipe on the points, max entry difference between build(recipe) and fit_matrix, determinant)`.

The tests require every recipe to reproduce its target to 1e-9 and to agree with the fitted matrix.
