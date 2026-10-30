# Puzzle: what does the best line even mean?

Fifty noisy measurements $(x_i, y_i)$ and a model $y \approx w_0 + w_1 x$. Fifty equations, two unknowns, and no line passes through all the points. Any line leaves **residuals** $r_i = y_i - w_0 - w_1 x_i$; least squares chooses the line that makes $\sum r_i^2$ as small as possible.

::::predict{id=p1 kind=choice answer=c}
At the least-squares line, which of these holds?

- Every residual is zero.
- Half the residuals are positive and half negative.
- The residuals sum to zero, and so does each residual multiplied by its $x_i$.
- The largest residual is as small as possible.

:::reveal
The residuals sum to zero, and $\sum x_i r_i = 0$ too. Those are two equations in the two unknowns, the **normal equations**, and they say the residual vector is perpendicular to the column of ones and to the column of $x$ values. Half positive and half negative is the median's property, not the mean's; making the largest residual small is a different problem altogether.
:::
::::

::::predict{id=p2 kind=numeric answer=0.5 tol=0.01}
Three points: $(0, 0)$, $(1, 1)$, $(2, 1)$. What is the slope of the least-squares line?

:::reveal
$0.5$. The means are $\bar x = 1$ and $\bar y = 2/3$; the slope is $\sum (x_i - \bar x)(y_i - \bar y) / \sum (x_i - \bar x)^2 = 1 / 2$, and the intercept is $\bar y - 0.5 \bar x = 1/6$. Check: the residuals are $-1/6$, $1/3$ and $-1/6$, which sum to 0, and $0 \cdot (-1/6) + 1 \cdot (1/3) + 2 \cdot (-1/6) = 0$.
:::
::::

Move the line by hand. The caption reports the two dot products, the residual with the column of ones and with the column of $x$. Try to make both zero at once, then snap to the least-squares line.

:::widget{name=ProjectionExplorer}
:::

## Questions to carry into the derivation

1. Why is the nearest point of a plane at the foot of a perpendicular?
2. How do "perpendicular to every column" and "smallest sum of squares" turn into the same equations?
3. What makes some bases of a subspace better than others for computing?
4. When do the normal equations give a wrong answer on a computer?
