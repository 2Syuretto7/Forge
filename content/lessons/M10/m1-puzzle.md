# Puzzle: four numbers that move the plane

A 2 by 2 grid of numbers

$$
A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}
$$

turns the unit square into a slanted parallelogram. Which numbers say where the corners go?

::::predict{id=p1 kind=choice answer=b}
Where does $A$ send the points $(1, 0)$ and $(0, 1)$?

- $(2, 1)$ and $(0, 1)$: the rows of $A$.
- $(2, 0)$ and $(1, 1)$: the columns of $A$.
- $(2, 0)$ and $(0, 1)$: the diagonal entries only.
- $(3, 0)$ and $(1, 1)$.

:::reveal
The columns. $A(1, 0) = (2 \cdot 1 + 1 \cdot 0,\ 0 \cdot 1 + 1 \cdot 0) = (2, 0)$, the first column, and $A(0, 1) = (1, 1)$, the second. A matrix is a list of where the basis vectors go, written as columns. Once you know those, linearity decides where every other point goes.
:::
::::

::::predict{id=p2 kind=numeric answer=2 tol=0.01}
The unit square has area 1. What is the area of its image, the parallelogram with sides $(2, 0)$ and $(1, 1)$?

:::reveal
Base 2, height 1: area 2. Every shape's area is multiplied by the same factor, 2, the **determinant** of $A$. Section 5 derives the formula $ad - bc$ for it.
:::
::::

In the widget the blue and green arrows are the images of $(1, 0)$ and $(0, 1)$, and the dashed circle becomes the solid ellipse. Set the four entries to 2, 1, 0, 1 and compare with your predictions; then find entries that turn the square without changing its shape.

:::widget{name=MatrixTransform a=2 b=1 c=0 d=1 svd=false}
:::

## Questions to carry into the derivation

1. Why does knowing where two vectors go fix where every vector goes?
2. If one matrix rotates and another shears, what does doing both mean, and does the order matter?
3. Which matrices can be undone?
4. Why is the area factor the same for every shape?
