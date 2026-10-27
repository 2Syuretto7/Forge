# Recall bridge: vectors, dot products and systems

This is the first lesson, so there are no earlier lessons to review. Instead, this bridge checks the high-school tools the lesson builds on. Work through it quickly; if any step feels shaky, slow down here rather than later.

## How every lesson works

Each lesson is a long arc of movements: a recall bridge, a puzzle, a derivation, a build, a scale-and-measure session, a break-it session, a plain-language explanation, and a capstone. Theory and practice each take about half the time. Exercises run real Python with NumPy in your browser; press **Check** to run the hidden tests.

## Three facts you will use constantly

A vector $x \in \mathbb{R}^d$ is a list of $d$ numbers. You can read it as a point or as an arrow from the origin. Two operations matter most.

The **dot product** $x^\top y = \sum_i x_i y_i$ measures how much two arrows point the same way. The **length** (Euclidean norm) is $\|x\| = \sqrt{x^\top x}$. Together they give the angle: $\cos\theta = \dfrac{x^\top y}{\|x\|\,\|y\|}$.

A **linear system** $Ax = b$ asks which combination of the columns of $A$ produces $b$. In two dimensions you solved these by elimination: subtract a multiple of one equation from the other.

::::derivation{id=d0 title="Warm-up: a dot product and an elimination"}
:::step
Let $x = (3, 4)$. Its length is $\sqrt{3^2 + 4^2} =$ [[5]].
:::
:::step
Let $y = (4, -3)$. The dot product $x^\top y = 3 \cdot 4 + 4 \cdot (-3) =$ [[0]], so the two vectors are perpendicular.
:::
:::step
Solve $x_1 + x_2 = 3$ and $x_1 - x_2 = 1$. Adding the equations gives $2x_1 = 4$, so $x_1 =$ [[2]].
:::
:::step
For a general scalar equation $a x = c$ with $a \neq 0$, the solution is $x =$ [[c/a]]. Keep this one in mind: when $a$ is tiny, a tiny change in $c$ moves $x$ a lot. The whole of Movement 1 grows out of that observation.
:::
::::

## What this lesson gives you

By the end you will have built, from scratch and in NumPy: projections, Gram-Schmidt and QR, least squares two ways, power iteration, the SVD, condition numbers, PCA and low-rank compression. Every later lesson uses at least one of these.

:::edge{to=L05 text="Least squares becomes linear regression with a Gaussian noise model."}
:::
