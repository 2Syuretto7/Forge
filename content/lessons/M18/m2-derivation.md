# Derivation: gradients, Jacobians and Hessians

## 1. Partial derivatives

For $f: \mathbb{R}^n \to \mathbb{R}$, the **partial derivative** $\partial f/\partial x_j$ is the ordinary derivative in $x_j$ with the other variables held fixed. Collected into a vector, they form the **gradient**

$$
\nabla f = \left(\frac{\partial f}{\partial x_1}, \dots, \frac{\partial f}{\partial x_n}\right) .
$$

For a smooth $f$ (continuous partial derivatives), $f$ is **differentiable**: near $x$,

$$
f(x + h) = f(x) + \nabla f(x) \cdot h + r(h), \qquad \frac{r(h)}{\|h\|} \to 0 .
$$

The gradient is the slope of the best linear approximation, as $f'$ was in one variable.

::::derivation{id=d1 title="A gradient by hand"}
:::step
For $f(x, y) = x^2 y + \sin y$, $\partial f/\partial x = 2xy$. At $(1, 2)$ it equals [[4]].
:::
:::step
$\partial f/\partial y = x^2 + \cos y$. At $(1, 0)$ it equals [[2]].
:::
::::

## 2. Directional derivatives and steepest ascent

The rate of change of $f$ at $x$ in the unit direction $u$ is the **directional derivative**: by the linear approximation,

$$
D_u f(x) = \lim_{t \to 0} \frac{f(x + tu) - f(x)}{t} = \nabla f(x) \cdot u .
$$

By Cauchy-Schwarz, $|\nabla f \cdot u| \leq \|\nabla f\|\,\|u\| = \|\nabla f\|$, with equality exactly when $u$ points along $\nabla f$. So **the gradient points in the direction of steepest ascent, and its length is that steepest slope**; $-\nabla f$ is steepest descent. Along a contour line $f$ is constant, so $\nabla f \cdot u = 0$ for the contour's direction: **the gradient is perpendicular to the contour lines**.

::::derivation{id=d2 title="Slopes in directions"}
:::step
With $\nabla f = (3, 4)$ and $u = (1, 0)$, $D_u f =$ [[3]].
:::
:::step
With $u = (0.6, -0.8)$, $D_u f = 1.8 - 3.2 =$ [[-1.4]]: this direction goes downhill.
:::
:::step
The steepest descent direction is $-\nabla f/\|\nabla f\| = (-0.6, -0.8)$, along which the slope is [[-5]].
:::
::::

## 3. The Jacobian: the best linear map

For $f: \mathbb{R}^n \to \mathbb{R}^m$, each output $f_i$ has a gradient. Stacking them as rows gives the $m \times n$ **Jacobian** matrix, $J_{ij} = \partial f_i / \partial x_j$, and

$$
f(x + h) \approx f(x) + J(x)\,h .
$$

Near $x$, $f$ acts like the linear map $J(x)$ (M10). Column $j$ of $J$ is how all outputs move when only $x_j$ moves. A gradient is the Jacobian of a function with one output, written as a column.

::::derivation{id=d3 title="A Jacobian by hand"}
:::step
$f(x, y) = (xy, \sin x)$ at $(0.5, 3)$: the first row is $(y, x) = (3, 0.5)$. The entry in row 2, column 1 is $\cos 0.5 \approx$ [[0.8776|tol=0.0005]].
:::
:::step
The entry in row 2, column 2 is [[0]], since $\sin x$ does not depend on $y$.
:::
::::

The widget shows a linear map acting on the plane. A nonlinear map looks like this near each point, with its Jacobian as the matrix, and a different matrix at each point.

:::widget{name=MatrixTransform a=1.2 b=0.4 c=-0.3 d=0.8 svd=false}
:::

## 4. The chain rule: multiply the Jacobians

If $g: \mathbb{R}^n \to \mathbb{R}^k$ and $f: \mathbb{R}^k \to \mathbb{R}^m$, the composition $f \circ g$ has Jacobian

$$
J_{f \circ g}(x) = J_f(g(x))\; J_g(x) ,
$$

an $(m \times k)(k \times n)$ product. The linear approximations compose, and composing linear maps multiplies their matrices (M10). For a scalar loss of a long chain of layers, $L = \ell(f_K(\dots f_1(x)))$, the gradient is a product of many Jacobians; the order in which they are multiplied decides the cost, which is M19's subject.

## 5. The Hessian and second-order Taylor

The **Hessian** of $f: \mathbb{R}^n \to \mathbb{R}$ is the matrix of second partial derivatives, $H_{ij} = \partial^2 f / \partial x_i \partial x_j$: the Jacobian of the gradient. For smooth $f$ it is symmetric (mixed partials commute). Second-order Taylor:

$$
f(x + h) \approx f(x) + \nabla f \cdot h + \tfrac12\, h^\top H h .
$$

At a critical point, $\nabla f = 0$ and the quadratic form $h^\top H h$ decides (M13): all eigenvalues of $H$ positive, a **minimum**; all negative, a **maximum**; both signs, a **saddle**, going up in some directions and down in others. If the largest eigenvalue is at most $L$ everywhere, the descent lemma of M16 holds in every direction: a gradient step with $\eta < 2/L$ lowers $f$.

::::derivation{id=d4 title="Classifying a critical point"}
:::step
$f(x, y) = x^2 + y^2 - 3xy$ has $\nabla f = (2x - 3y, 2y - 3x)$, zero at the origin. Its Hessian is $\begin{pmatrix} 2 & -3 \\ -3 & 2 \end{pmatrix}$ with eigenvalues $2 \pm 3$; the negative one is [[-1]].
:::
:::step
So the origin is a [[word:saddle/saddle point]], although along both axes $f = x^2$ or $y^2$ looks like a minimum: along the diagonal $f(t, t) = -t^2$.
:::
::::

::::predict{id=p3 kind=choice answer=a}
The gradient of $f(x) = \frac12 x^\top A x$ for a square matrix $A$ that is not symmetric. Which is it?

- $\frac12 (A + A^\top)\,x$.
- $Ax$.
- $A^\top x$.
- $2Ax$.

:::reveal
$\frac12 (A + A^\top)x$. Only the symmetric part of $A$ contributes to the quadratic form, since $x^\top A x = x^\top A^\top x$. Writing $Ax$ is a classic bug that a gradient check catches at once; for symmetric $A$, the usual case of Hessians and covariances, the two agree.
:::
::::

## 6. Checking gradients numerically

Every hand-derived gradient should be checked against central differences, as M15 did in one variable: perturb one input at a time, compare with the formula through a relative error, and expect about $10^{-8}$ or better in float64. A check costs $2n$ evaluations for $n$ inputs: affordable for testing, hopeless for training, which is why M19 computes gradients exactly by automatic differentiation.

::::derivation{id=d5 title="The cost of checking"}
:::step
Central differences for a function of $10^4$ inputs need [[20000]] evaluations.
:::
::::

:::edge{to=M19 text="the chain rule as a product of Jacobians, evaluated in the cheap order: automatic differentiation."}
:::

:::edge{to=M20 text="the Jacobian determinant measures how a map stretches area, and so how it changes densities."}
:::

:::edge{to=M28 text="convexity in many variables: a positive semidefinite Hessian everywhere."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Gradient | vector of partial derivatives; best linear approximation | slopes of losses |
| Directional derivative | $\nabla f \cdot u$, at most $\|\nabla f\|$ | steepest ascent and descent |
| Contours | gradient perpendicular to them | read a landscape |
| Jacobian | $J_{ij} = \partial f_i / \partial x_j$; $f(x + h) \approx f(x) + Jh$ | layers as local linear maps |
| Chain rule | $J_{f \circ g} = J_f J_g$ | backpropagation (M19) |
| Hessian | symmetric matrix of second partials | minimum, maximum or saddle |
| Gradient check | central differences, relative error | trust a derivation |
