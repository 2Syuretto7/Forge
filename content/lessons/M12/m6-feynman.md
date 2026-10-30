# Explain it plainly: the right angle

Explain why the shortest path from a point to a plane meets the plane at a right angle, and why that solves least squares.

Guidelines:

- Write 150 to 400 words.
- Use a physical picture: a lamp above a table, a ladder against a wall.
- Say what the point, the plane and the right angle are in a line fit.
- No matrices needed.

:::feynman{id=f1 prompt="Explain why the shortest path from a point to a plane meets it at a right angle, and why that solves least squares." key_points="Any other point of the plane is farther, because its distance squared adds the squared distance along the plane, by Pythagoras|So the nearest point is where the connecting segment is perpendicular to the plane|In least squares the plane is the set of all predictions the model can make|The data are the point, and the best prediction is the foot of the perpendicular|Perpendicular to the plane means the residuals have zero dot product with every input column, which are the normal equations"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that if A^T (A x_hat - b) = 0, then x_hat minimizes ||Ax - b|| over all x, and that the minimizer is unique when the columns of A are independent." key_points="Writes any x as x_hat + d|Expands ||A x_hat - b + A d||^2 as ||A x_hat - b||^2 + 2 d^T A^T (A x_hat - b) + ||A d||^2|Uses the hypothesis to make the middle term zero|Concludes ||Ax - b||^2 >= ||A x_hat - b||^2, with excess ||Ad||^2|Equality needs Ad = 0, and independent columns force d = 0, so the minimizer is unique"}
:::
