# Derivation: vectors, the dot product and projection

## 1. Vectors

A **vector** in $\mathbb{R}^d$ is a list of $d$ real numbers, $x = (x_1, \dots, x_d)$. Read it two ways: as a **point** in $d$-dimensional space, or as an **arrow** from the origin to that point. Both readings matter. Embeddings are points (similar words are nearby); gradients (M18) are arrows (they point uphill).

Vectors add coordinate by coordinate, and a number (a **scalar**) multiplies every coordinate:

$$
x + y = (x_1 + y_1, \dots, x_d + y_d), \qquad c\,x = (c x_1, \dots, c x_d) .
$$

As arrows: adding places one arrow at the tip of the other; scaling stretches, and a negative scalar also reverses.

## 2. Length

In the plane, Pythagoras gives the length $\sqrt{x_1^2 + x_2^2}$. In three dimensions, apply Pythagoras twice: the diagonal of a box with sides $x_1, x_2, x_3$ has squared length $(x_1^2 + x_2^2) + x_3^2$. By induction (M05), in $d$ dimensions

$$
\|x\| = \sqrt{x_1^2 + x_2^2 + \dots + x_d^2} .
$$

::::derivation{id=d1 title="Length in any dimension"}
:::step
The length of $(1, 2, 2)$ is $\sqrt{1 + 4 + 4} =$ [[3]].
:::
:::step
Dividing a nonzero vector by its length gives a **unit vector**, of length 1, pointing the same way. The unit vector along $(1, 2, 2)$ has first coordinate [[1/3]].
:::
:::step
Scaling multiplies length: $\|c\,x\| = |c|\,\|x\|$. The length of $-3 \cdot (1, 2, 2)$ is [[9]].
:::
::::

## 3. The dot product, two ways

The **dot product** of two vectors is the sum of the products of their coordinates:

$$
x \cdot y = x_1 y_1 + x_2 y_2 + \dots + x_d y_d .
$$

So $x \cdot x = \|x\|^2$. It is symmetric ($x \cdot y = y \cdot x$) and linear in each argument ($(a x + b z) \cdot y = a\, x \cdot y + b\, z \cdot y$), both straight from the definition.

Here is the surprise. This sum of products, which seems to care about coordinates, depends only on the lengths of the arrows and the angle between them. The proof is the law of cosines, redone with the dot product.

::::derivation{id=d2 title="Why the dot product measures the angle"}
:::step
The arrows $x$, $y$ and $x - y$ form a triangle. Expanding with linearity, $\|x - y\|^2 = (x - y) \cdot (x - y) = \|x\|^2 + \|y\|^2 - 2\,x \cdot y$. For $x = (3, 0)$ and $y = (0, 4)$ this is $9 + 16 - 0 =$ [[25]].
:::
:::step
The law of cosines says the side opposite an angle $t$, between sides of lengths $L$ and $M$, has squared length $L^2 + M^2 - 2LM\cos t$. Comparing the two expressions for $\|x - y\|^2$, the dot product is $x \cdot y =$ [[L*M*cos(t)]].
:::
:::step
So $\cos t = \dfrac{x \cdot y}{\|x\|\,\|y\|}$. For $x = (1, 1)$ and $y = (1, 0)$ the dot product is 1 and the lengths are $\sqrt{2}$ and 1, so $\cos t =$ [[1/sqrt(2)]], an angle of $45^\circ$.
:::
::::

So in any dimension, the angle between two vectors is **defined** by $\cos t = x \cdot y / (\|x\|\,\|y\|)$, the **cosine similarity**. Perpendicular means dot product 0, written $x \perp y$.

## 4. Cauchy-Schwarz

The definition only makes sense if $x \cdot y / (\|x\|\,\|y\|)$ always lies between $-1$ and $1$. In the plane that is obvious, since it is a cosine. In 300 dimensions it needs a proof, and it is one of the most used inequalities in mathematics.

::::derivation{id=d3 title="The Cauchy-Schwarz inequality"}
:::step
For every real $t$, a squared length is never negative: $\|x - t\,y\|^2 \geq 0$. Expanding, writing $A = \|x\|^2$, $B = \|y\|^2$ and $D = x \cdot y$, this says $A - 2tD + t^2 B \geq 0$ for every $t$.
:::
:::step
The quadratic in $t$ is smallest at $t = D/B$ (complete the square, M02). Its value there is [[A - D^2/B]], and it must still be at least 0.
:::
:::step
Multiplying by $B > 0$: $D^2 \leq AB$, that is $(x \cdot y)^2 \leq \|x\|^2 \|y\|^2$. Equality holds exactly when $x - t\,y = 0$ for some $t$, that is when the vectors are [[word:parallel/collinear/multiples of each other]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
Can the dot product of two unit vectors in 1,000 dimensions exceed 1?

- Yes, if many coordinates are large.
- Yes, but only slightly, through rounding.
- No: by Cauchy-Schwarz it is at most $\|x\|\,\|y\| = 1$, with equality only when the vectors are the same.
- Only for vectors with negative coordinates.

:::reveal
No. Cauchy-Schwarz bounds it by the product of the lengths, in every dimension, and equality needs the vectors to be parallel. In floating point a computed cosine can come out as $1.0000000000000002$ for parallel vectors, which is why code clips it before calling arccos; the mathematics is not to blame.
:::
::::

A consequence: the **triangle inequality** $\|x + y\| \leq \|x\| + \|y\|$. Expand $\|x + y\|^2 = \|x\|^2 + 2x \cdot y + \|y\|^2$ and bound $x \cdot y$ by $\|x\|\,\|y\|$.

## 5. Projection onto a line

How much of $b$ points along $a$? Drop a perpendicular from the tip of $b$ to the line through $a$. The foot is $p = t\,a$ for the $t$ that makes $b - t\,a$ perpendicular to $a$.

::::derivation{id=d4 title="Projecting onto a line"}
:::step
$(b - t\,a) \cdot a = 0$ gives $b \cdot a - t\,(a \cdot a) = 0$, so $t = \dfrac{a \cdot b}{a \cdot a}$. For $a = (1, 0)$ and $b = (3, 4)$, $t =$ [[3]].
:::
:::step
The projection is $p = (3, 0)$ and the residual $b - p = (0, 4)$. Its dot product with $a$ is [[0]]: the residual is perpendicular to the line.
:::
::::

The length of the projection is $\|b\| \cos t$: the dot product with a unit vector measures how far $b$ reaches along it. Projection onto many directions at once (a plane, a subspace) is least squares, in M12.

## 6. Other ways to measure size

The length $\|x\|$ is the **L2 norm**. Two others are common:

$$
\|x\|_1 = |x_1| + \dots + |x_d|, \qquad \|x\|_\infty = \max_i |x_i| .
$$

All three are **norms**: zero only for the zero vector, scaled by $|c|$ when the vector is scaled by $c$, and satisfying the triangle inequality. They measure different things: the L1 norm is the total amount, the L-infinity norm the worst coordinate. Regularization (L06) penalizes L2 or L1 norms of weights; gradient clipping (L19) caps an L2 norm.

::::derivation{id=d5 title="Three norms of one vector"}
:::step
For $x = (3, -4)$: $\|x\|_1 = 7$, $\|x\|_\infty = 4$ and $\|x\|_2 =$ [[5]].
:::
:::step
In general $\|x\|_\infty \leq \|x\|_2 \leq \|x\|_1$. For $x = (1, 1, \dots, 1)$ in $d$ dimensions, $\|x\|_2 = \sqrt{d}$ and $\|x\|_1 = d$; with $d = 100$ the L1 norm is [[10]] times the L2 norm.
:::
::::

Each norm has its own **unit ball**, the vectors of norm at most 1: a diamond for L1, a circle for L2, a square for L-infinity. Choose a ball in the widget and move $x$ onto its edge: the caption shows that norm reading exactly 1 while the other two do not.

:::widget{name=VectorPlayground x1=0.6 x2=0.4 y1=-1 y2=1.5 proj=false ball=l1}
:::

In the next lesson a machine takes vectors to vectors, and every one of its outputs is a dot product.

:::edge{to=M10 text="a matrix times a vector is a list of dot products, one per row."}
:::

:::edge{to=M34 text="in high dimension random vectors are almost perpendicular, the fact behind the puzzle and behind dividing attention scores by the square root of d."}
:::

## Summary

| Idea | Formula | Use |
| --- | --- | --- |
| Length | $\|x\| = \sqrt{x \cdot x}$ | distances between embeddings |
| Dot product | $x \cdot y = \sum x_i y_i = \|x\|\,\|y\|\cos t$ | similarity, projections |
| Cosine similarity | $x \cdot y / (\|x\|\,\|y\|)$ | compare directions |
| Cauchy-Schwarz | $\lvert x \cdot y \rvert \leq \|x\|\,\|y\|$ | cosines lie in $[-1, 1]$ |
| Projection | $\frac{a \cdot b}{a \cdot a}\, a$ | the part of $b$ along $a$ |
| Norms | L1, L2, L-infinity | sizes of weights and errors |
