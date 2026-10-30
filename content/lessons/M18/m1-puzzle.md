# Puzzle: steepest on a foggy hillside

You stand on a hillside in fog. You cannot see the hill, but you can feel the slope under your feet: one step east raises you by 3 cm, one step north by 4 cm.

::::predict{id=p1 kind=choice answer=b}
Which way is steepest uphill?

- North, the larger of the two slopes.
- Toward east 3, north 4: the direction of the vector of slopes.
- North-east, halfway between.
- It cannot be told without seeing the hill.

:::reveal
Along $(3, 4)$, the **gradient**. A step in the unit direction $u = (u_1, u_2)$ raises you by $3u_1 + 4u_2 = (3, 4) \cdot u$, a dot product, which by Cauchy-Schwarz (M09) is largest when $u$ points along $(3, 4)$. Two measured slopes decide every direction, as long as the hill is smooth.
:::
::::

::::predict{id=p2 kind=numeric answer=5 tol=0.01}
How many centimetres does one step in the steepest direction raise you?

:::reveal
5: the length of $(3, 4)$. Stepping along the gradient's direction gives $(3, 4) \cdot (0.6, 0.8) = 5$, the largest possible rise for a unit step. Stepping perpendicular to it, along $(-4, 3)$, gives 0: you walk along a contour line.
:::
::::

Move the point and turn your direction $u$. The caption reports the slope in your direction, never more than the gradient's length; the arrows on the grid are gradients, crossing every contour at a right angle.

:::widget{name=GradientField f=bowl x=1 y=0.5 phi=45}
:::

## Questions to carry into the derivation

1. How do slopes along the axes determine the slope in every direction?
2. What replaces the derivative for a function with several outputs?
3. How do these local linear maps compose?
4. What does the second derivative become, and how does it tell a minimum from a saddle?
