# Derivation: Taylor, extrema, Newton and gradient descent

## 1. The mean value theorem

If $f$ is differentiable on an interval from $a$ to $b$, some point $c$ between them has

$$
f'(c) = \frac{f(b) - f(a)}{b - a} :
$$

somewhere the instantaneous slope equals the average slope. (If you averaged 60 km/h over a trip, at some instant the speedometer read exactly 60.) Consequences: a function with $f' = 0$ everywhere is constant, one with $f' > 0$ is increasing, and $|f(b) - f(a)| \leq \max|f'| \cdot |b - a|$.

## 2. Taylor polynomials with remainder

The polynomial of degree $n$ that matches $f$ and its first $n$ derivatives at $a$ is

$$
T_n(x) = f(a) + f'(a)(x - a) + \frac{f''(a)}{2!}(x - a)^2 + \dots + \frac{f^{(n)}(a)}{n!}(x - a)^n .
$$

**Taylor's theorem** (the mean value theorem applied repeatedly) says the error is the next term, evaluated at some unknown point $\xi$ between $a$ and $x$:

$$
f(x) - T_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x - a)^{n+1} .
$$

So if $|f^{(n+1)}| \leq M$ on the interval, the error is at most $M|x - a|^{n+1}/(n+1)!$. For $\sin$ and $\cos$, $M = 1$; for $e^x$ on $[0, x]$, $M = e^x$.

::::derivation{id=d1 title="Bounding a Taylor error"}
:::step
Around $a = 0$, $\sin$ has derivatives $0, 1, 0, -1, \dots$, so $T_3(x) = x - x^3/6$. At $x = 0.1$, $T_3 = 0.1 - 0.001/6 \approx$ [[0.0998333|tol=1e-6]].
:::
:::step
$T_3 = T_4$ for the sine, so the remainder bound uses $n = 4$: $|x|^5/5! = 10^{-5}/120 \approx$ [[8.3e-8|tol=1e-9]].
:::
::::

## 3. Critical points and the second-derivative test

At an interior minimum or maximum of a differentiable function, $f'(x) = 0$: otherwise a small step one way would go lower and the other way higher. Such points are **critical points**. Which kind? Taylor to second order at a critical point $c$:

$$
f(c + h) = f(c) + \tfrac12 f''(c)\,h^2 + (\text{smaller}) .
$$

If $f''(c) > 0$ the function rises on both sides: a **minimum**. If $f''(c) < 0$: a **maximum**. If $f''(c) = 0$ the test says nothing, and the next nonzero derivative decides.

::::derivation{id=d2 title="Classifying critical points"}
:::step
$f(x) = x^3 - 3x$ has $f'(x) = 3x^2 - 3$, so its critical points are $\pm 1$. $f''(x) = 6x$, so $f''(1) =$ [[6]], and 1 is a minimum.
:::
:::step
The minimum value is $f(1) =$ [[-2]].
:::
::::

::::predict{id=p3 kind=choice answer=c}
What does the second-derivative test say about $f(x) = x^4$ at $x = 0$?

- A minimum, because $f'' > 0$.
- A maximum.
- Nothing: $f''(0) = 0$, although 0 is in fact a minimum.
- Not a critical point.

:::reveal
Nothing: $f'(0) = f''(0) = f'''(0) = 0$, and only $f''''(0) = 24 > 0$ shows the minimum. The same test applied to $x^3$ also gives $f''(0) = 0$, and there 0 is no extremum at all. Flat regions like these slow optimizers to a crawl.
:::
::::

## 4. Convexity

$f$ is **convex** on an interval if every chord lies above the graph: $f(tx + (1 - t)y) \leq t f(x) + (1 - t) f(y)$ for $t \in [0, 1]$. For twice-differentiable $f$ this is equivalent to $f'' \geq 0$. Convex functions have no local minima that are not global, and a critical point of a convex function is a global minimum. M28 builds the theory in many dimensions; here it is a property you can read off the second derivative.

::::derivation{id=d3 title="Minimizing a convex function"}
:::step
$f(x) = e^x - 2x$ has $f''(x) = e^x > 0$, so it is convex. Its critical point solves $e^x = 2$, at $x =$ [[ln(2)]], the global minimum.
:::
:::step
The minimum value is $2 - 2\ln 2 \approx$ [[0.6137|tol=0.001]].
:::
::::

## 5. Newton's method

To solve $f(x) = 0$, replace $f$ by its tangent at the current guess and solve that instead:

$$
x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)} .
$$

Near a root $r$ with $f'(r) \neq 0$, Taylor's theorem at $x_k$ gives $0 = f(r) = f(x_k) + f'(x_k)(r - x_k) + \frac12 f''(\xi)(r - x_k)^2$. Dividing by $f'(x_k)$ and using the definition of $x_{k+1}$:

$$
r - x_{k+1} = -\frac{f''(\xi)}{2f'(x_k)}(r - x_k)^2 .
$$

The error is **squared** at each step, up to a constant: **quadratic convergence**, which doubles the number of correct digits. Bisection, which halves a bracket, is **linear**: a fixed factor per step. The secant method, which replaces $f'$ by the slope through the last two points, has order $\frac{1 + \sqrt 5}{2} \approx 1.618$, **superlinear**, with one function evaluation per step instead of two.

To **minimize** $g$, apply Newton to $g'$: $x_{k+1} = x_k - g'(x_k)/g''(x_k)$, which jumps to the minimum of the local quadratic model.

::::derivation{id=d4 title="Newton for a square root"}
:::step
For $f(x) = x^2 - 2$, $f'(x) = 2x$, and the Newton step is $x - \frac{x^2 - 2}{2x} = \frac12\left(x + \frac{2}{x}\right)$. From $x = 17/12$ it gives $577/408 \approx$ [[1.4142157|tol=1e-6]].
:::
:::step
The constant $\frac{f''(r)}{2f'(r)} = \frac{2}{4\sqrt 2} \approx 0.354$. With error $2.45 \times 10^{-3}$, the next error is about $0.354 \times (2.45 \times 10^{-3})^2 \approx$ [[2.1e-6|tol=1e-7]].
:::
::::

## 6. Gradient descent and the step-size limit

Gradient descent ignores the second derivative and steps against the first: $x_{k+1} = x_k - \eta f'(x_k)$. On the quadratic $f(x) = \frac{L}{2}x^2$, $f'(x) = Lx$ and

$$
x_{k+1} = (1 - \eta L)\,x_k .
$$

It converges exactly when $|1 - \eta L| < 1$, that is $0 < \eta < 2/L$. Below $1/L$ it creeps monotonically; between $1/L$ and $2/L$ it overshoots and oscillates while shrinking; above $2/L$ the oscillation grows. For a general $f$ with $|f''| \leq L$, the **descent lemma** (Taylor with remainder) gives $f(x - \eta f'(x)) \leq f(x) - \eta\big(1 - \frac{L\eta}{2}\big) f'(x)^2$, so every step with $\eta < 2/L$ lowers $f$. Linear convergence, at rate $|1 - \eta L|$ near the minimum: no squaring, which is the price of not using $f''$.

::::derivation{id=d5 title="The largest safe step"}
:::step
For $f(x) = 2x^2$, $L = 4$, so gradient descent converges for $\eta$ below [[0.5]].
:::
:::step
With $\eta = 0.4$, each step multiplies $x$ by $1 - 0.4 \times 4 = -0.6$: the iterates alternate in sign and shrink by the factor [[0.6]].
:::
::::

:::edge{to=M18 text="the Hessian matrix and second-order Taylor in many variables."}
:::

:::edge{to=M25 text="maximum likelihood is an optimization, and Newton's method on it is Fisher scoring."}
:::

:::edge{to=M29 text="the step-size limit 2/L and linear rates, in any dimension."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Mean value theorem | $f'(c)$ = average slope | bounds, monotonicity |
| Taylor | error = next term at some $\xi$ | approximate functions |
| Second-derivative test | $f'' > 0$ min, $< 0$ max, $= 0$ silent | classify critical points |
| Convexity | $f'' \geq 0$; chords above the graph | every critical point is global |
| Newton | $x - f/f'$; error squared | fast roots, Newton minimization |
| Secant, bisection | order 1.618; linear with factor 1/2 | no derivative; guaranteed bracket |
| Gradient descent | rate $|1 - \eta L|$; needs $\eta < 2/L$ | the workhorse of training |
