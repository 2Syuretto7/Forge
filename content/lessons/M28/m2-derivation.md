# Derivation: convexity and the geometry of optimization

## 1. Convex sets and convex functions

A set $C$ is **convex** if it contains the segment between any two of its points. A function is **convex** if its graph lies on or below every chord:

$$
f\big(tx + (1 - t)y\big) \le t f(x) + (1 - t) f(y) \qquad \text{for all } x, y \text{ and } t \in [0, 1] ,
$$

equivalently, the region above its graph is a convex set. Examples: every norm, $e^x$, $x^2$, $-\log x$, $\max_i x_i$, log-sum-exp, and every affine function (which is convex and concave). Convexity is preserved by nonnegative sums, by pointwise maxima, by composition with an affine map, and by $g(h(x))$ when $h$ is convex and $g$ is convex and nondecreasing.

**Why it matters.** A convex function has no bad local minima: if $x$ were a local minimum and $f(y) < f(x)$, the chord inequality would put points arbitrarily close to $x$, on the segment toward $y$, below $f(x)$.

::::derivation{id=d1 title="A chord of the exponential"}
:::step
For $f(x) = e^x$ at $x = 0$ and $y = 2$, the midpoint of the chord has height $\frac{1 + e^2}{2} \approx$ [[4.195|tol=0.002]].
:::
:::step
The function at the midpoint is $e^1 \approx 2.718$, below the chord, as convexity requires. The gap, about [[1.477|tol=0.002]], is a Jensen gap of Section 3.
:::
::::

## 2. First- and second-order conditions

For differentiable $f$, convexity is equivalent to lying above every tangent plane:

$$
f(y) \ge f(x) + \nabla f(x)^\top (y - x) \qquad \text{for all } x, y .
$$

So a point with $\nabla f(x) = 0$ is a **global** minimum: the tangent plane there is flat and the whole function lies above it. For twice-differentiable $f$, convexity is equivalent to a positive semidefinite Hessian everywhere, $\nabla^2 f(x) \succeq 0$, which by M13 means every eigenvalue is at least 0.

::::predict{id=p3 kind=choice answer=b}
Which of these is guaranteed to be convex for any convex $f$ and $g$?

- $f \cdot g$
- $\max(f, g)$
- $f - g$
- $f(g(x))$

:::reveal
$\max(f, g)$: the region above the maximum is the intersection of the regions above each, and intersections of convex sets are convex. The product fails ($x \cdot x^{-1}$ restricted suitably, or $x^2 \cdot e^{-x}$), the difference fails ($0 - x^2$), and the composition needs $f$ nondecreasing as well: $(x^2 - 1)^2$ is $u^2$ of the convex $x^2 - 1$, and it has two minima.
:::
::::

::::derivation{id=d2 title="Reading a Hessian"}
:::step
$f(x, y) = x^2 + xy + y^2$ has Hessian $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, whose smallest eigenvalue is [[1]], so $f$ is convex, indeed strongly convex.
:::
:::step
Log-sum-exp has Hessian $\operatorname{diag}(p) - pp^\top$, the covariance matrix of a one-hot vector drawn with probabilities $p$. For $p = (\frac12, \frac12)$, its eigenvalues are $\frac12$ and [[0]]: convex, but flat along $(1, 1)$, where adding a constant to every logit changes nothing.
:::
::::

## 3. Jensen's inequality

For convex $f$ and any random variable $X$,

$$
f(\mathbb{E}X) \le \mathbb{E}f(X) .
$$

It is the chord inequality averaged over many points: the function of the average lies below the average of the function. Consequences you have met or will meet: $\operatorname{Var}X = \mathbb{E}X^2 - (\mathbb{E}X)^2 \ge 0$ ($f = x^2$); the arithmetic mean is at least the geometric mean ($f = -\log$); $\mathbb{E}[1/\bar x] > 1/\mathbb{E}\bar x$, which biased M25's exponential-rate MLE; and Gibbs' inequality $\mathrm{KL} \ge 0$ (M27), with $f = -\log$ applied to $q/p$.

::::derivation{id=d3 title="Means of 1 and 9"}
:::step
The arithmetic mean of 1 and 9 is 5 and the geometric mean is [[3]], smaller, as Jensen's inequality for $-\log$ says.
:::
::::

## 4. Smoothness, strong convexity and the condition number

Two numbers bound the curvature of $f$ in every direction: $f$ is **$L$-smooth** if $\nabla^2 f \preceq L I$ and **$\mu$-strongly convex** if $\nabla^2 f \succeq \mu I$. For the quadratic $f(x) = \frac12 x^\top A x - b^\top x$, $L = \lambda_{\max}(A)$, $\mu = \lambda_{\min}(A)$, and their ratio is the **condition number** $\kappa = L/\mu$. Its level sets are ellipses with half-axes proportional to $1/\sqrt{\lambda_i}$, so $\sqrt\kappa$ is their elongation.

Gradient descent $x \leftarrow x - \eta\nabla f(x)$ on the quadratic moves the error $e = x - x^\star$ by $e \leftarrow (I - \eta A)e$: along each eigenvector the error is multiplied by $1 - \eta\lambda_i$. So:

- it converges exactly when every $\lvert 1 - \eta\lambda_i\rvert < 1$, that is $\eta < 2/L$;
- with $\eta = 1/L$ the slowest factor is $1 - 1/\kappa$;
- the best fixed step $\eta = 2/(L + \mu)$ balances the two ends of the spectrum at $\rho = \frac{\kappa - 1}{\kappa + 1}$;
- reaching relative error $\varepsilon$ takes about $\frac{\kappa}{2}\log\frac{1}{\varepsilon}$ steps: proportional to the condition number.

The same rates hold for any $L$-smooth, $\mu$-strongly convex function, up to constants, because near its minimum it looks like its quadratic Taylor model.

::::derivation{id=d4 title="Counting steps"}
:::step
$A = \operatorname{diag}(1, 100)$ has condition number [[100]].
:::
:::step
With the best step the error shrinks per step by $\frac{99}{101} \approx$ [[0.9802|tol=0.0001]].
:::
:::step
To shrink it by $10^6$ takes $\lceil\ln 10^{-6}/\ln(99/101)\rceil =$ [[691|tol=1]] steps.
:::
::::

:::edge{to=L05 text="the step-size limit 2/L and the condition number in network training."}
:::

:::edge{to=M29 text="momentum and Nesterov change the dependence on kappa to sqrt(kappa)."}
:::

## 5. Convex negative log-likelihoods

An **exponential family** has densities $p(x \mid \theta) = h(x)\exp\big(\theta^\top T(x) - A(\theta)\big)$: Bernoulli, categorical, Gaussian, Poisson and exponential all fit. The log-partition $A(\theta)$ has gradient $\mathbb{E}_\theta[T(X)]$ and Hessian $\operatorname{Cov}_\theta[T(X)] \succeq 0$, so it is convex, and the negative log-likelihood of data, $nA(\theta) - \theta^\top\sum_i T(x_i)$, is convex in $\theta$. Logistic regression and softmax regression are of this form with $\theta$ linear in the weights, which is why they have a single global optimum and why their losses in L01 never trap gradient descent.

:::edge{from=M25 text="negative log-likelihoods of exponential families are convex."}
:::

## 6. Lagrange multipliers

To minimize $f(x)$ subject to $g(x) = 0$, note that at a constrained minimum the gradient of $f$ cannot have a component along the constraint surface, or moving along it would decrease $f$. So $\nabla f$ is perpendicular to the surface, parallel to $\nabla g$:

$$
\nabla f(x) + \lambda\nabla g(x) = 0, \qquad g(x) = 0 .
$$

With $m$ constraints there is one multiplier for each. The multiplier measures sensitivity: $\lambda$ is minus the rate at which the optimal value changes as the constraint level moves. For a convex $f$ and affine constraints the conditions are also sufficient. For a quadratic with linear constraints they form one linear system; for entropy with a mean constraint they give the Gibbs distribution $p_k \propto e^{-\beta k}$.

::::derivation{id=d5 title="The closest point on a line"}
:::step
Minimize $x^2 + y^2$ subject to $x + y = 1$: the conditions $2x + \lambda = 0$, $2y + \lambda = 0$ give $x = y$, so $x = y =$ [[0.5]].
:::
:::step
Then $\lambda = -2x =$ [[-1]], and the minimum value $\frac12$ changes at rate $-\lambda = 1$ per unit change of the constraint level: indeed $(c/2)^2 \cdot 2 = c^2/2$ has derivative $c = 1$ at $c = 1$.
:::
::::

:::edge{to=M30 text="duality and the KKT conditions for inequality constraints."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Convex function | graph below every chord | no bad local minima |
| First order | $f(y) \ge f(x) + \nabla f(x)^\top(y - x)$ | zero gradient is optimal |
| Second order | $\nabla^2 f \succeq 0$ | test by eigenvalues |
| Jensen | $f(\mathbb{E}X) \le \mathbb{E}f(X)$ | AM-GM, KL $\ge 0$, biases |
| Condition number | $\kappa = L/\mu$, eigenvalue ratio of the Hessian | difficulty of a problem |
| Gradient descent | converges for $\eta < 2/L$, about $\frac\kappa2\log\frac1\varepsilon$ steps | iteration counts |
| Exponential families | log-partition convex, NLL convex | logistic and softmax regression |
| Lagrange | $\nabla f + \lambda\nabla g = 0$, $\lambda$ a sensitivity | equality constraints |
