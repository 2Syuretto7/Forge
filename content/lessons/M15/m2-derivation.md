# Derivation: limits and derivatives

## 1. The limit of a function

$\lim_{x \to a} f(x) = L$ means: for every $\varepsilon > 0$ there is a $\delta > 0$ such that $|f(x) - L| < \varepsilon$ whenever $0 < |x - a| < \delta$. The value at $a$ itself does not matter, and need not exist. That is why the definition says $0 < |x - a|$.

Example: $f(x) = \frac{x^2 - 1}{x - 1}$ is undefined at 1, but for $x \neq 1$ it equals $x + 1$, so the limit at 1 is 2.

::::derivation{id=d1 title="Finding a delta"}
:::step
For $x \neq 1$, $\left|\frac{x^2 - 1}{x - 1} - 2\right| = |x + 1 - 2| = |x - 1|$. To make this smaller than $\varepsilon = 0.01$ it suffices to take $\delta =$ [[0.01]].
:::
:::step
For $f(x) = 3x + 1$ near $a = 2$ the limit is 7, and $|3x + 1 - 7| = 3|x - 2|$. For a tolerance $\varepsilon$, the threshold that works is $\delta =$ [[epsilon/3]], writing $\varepsilon$ as `epsilon`.
:::
::::

Limits obey the obvious laws: the limit of a sum, product or quotient (with a nonzero denominator) is the sum, product or quotient of the limits. Each is proved by splitting the tolerance, as for sequences in M05.

## 2. Continuity

$f$ is **continuous** at $a$ when $\lim_{x \to a} f(x) = f(a)$: no jump, no hole, no blow-up. Polynomials, $e^x$, $\sin x$ and $\ln x$ (for $x > 0$) are continuous wherever they are defined, and sums, products and compositions of continuous functions are continuous. A step function is not continuous at its step; $|x|$ and the ReLU are continuous everywhere, corners included.

## 3. The derivative: the best local linear approximation

The **derivative** of $f$ at $a$ is the limit of the slopes of secants:

$$
f'(a) = \lim_{h \to 0} \frac{f(a + h) - f(a)}{h} .
$$

When it exists, $f$ is **differentiable** at $a$, and

$$
f(a + h) = f(a) + f'(a)\,h + r(h), \qquad \frac{r(h)}{h} \to 0 .
$$

The line $f(a) + f'(a)h$ is the **best linear approximation** near $a$: its error shrinks faster than $h$ itself, and no other slope achieves that. This is the zooming of the puzzle, and it is the definition that generalizes to many variables in M18. A differentiable function is continuous, since $f(a + h) - f(a) = h \cdot (\text{difference quotient}) \to 0 \cdot f'(a) = 0$.

::::derivation{id=d2 title="Derivatives from the definition"}
:::step
$\frac{(a + h)^2 - a^2}{h} = 2a + h$, whose limit as $h \to 0$ is [[2*a]].
:::
:::step
$(a + h)^3 = a^3 + 3a^2h + 3ah^2 + h^3$, so the difference quotient of $x^3$ is $3a^2 + 3ah + h^2$, with limit [[3*a^2]].
:::
:::step
In general $(a + h)^n = a^n + n a^{n-1} h + (\text{terms with } h^2)$, so the derivative of $x^n$ is $n x^{n-1}$. The derivative of $x^7$ at $x = 1$ is [[7]].
:::
::::

## 4. The rules, proved

**Sum:** $(f + g)' = f' + g'$, from the limit of a sum.

**Product:** add and subtract $f(a + h)g(a)$:

$$
\frac{f(a+h)g(a+h) - f(a)g(a)}{h} = f(a + h)\,\frac{g(a + h) - g(a)}{h} + g(a)\,\frac{f(a + h) - f(a)}{h} \to f(a)g'(a) + g(a)f'(a),
$$

using that $f$ is continuous at $a$.

**Chain:** if $u = g(x)$ and $y = f(u)$, a change $h$ in $x$ changes $u$ by about $g'(x)h$, which changes $y$ by about $f'(u) \cdot g'(x)h$. So $(f \circ g)'(x) = f'(g(x))\,g'(x)$: the slopes of the stages multiply. (The careful proof uses the linear approximation of Section 3 for each stage.)

**Quotient:** write $f/g = f \cdot (1/g)$, and $(1/g)' = -g'/g^2$ by the chain rule.

::::derivation{id=d3 title="Using the rules"}
:::step
By the product rule, the derivative of $x^2 \sin x$ is $2x \sin x + x^2$ times [[cos(x)]].
:::
:::step
By the chain rule, the derivative of $\sin(x^2)$ is [[2*x*cos(x^2)]].
:::
::::

::::predict{id=p3 kind=choice answer=a}
Is $f(x) = x\,|x|$ differentiable at 0?

- Yes, with $f'(0) = 0$: the corner of $|x|$ is flattened by the factor $x$.
- No: it contains $|x|$, which has a corner at 0.
- Only from the right.
- Yes, with $f'(0) = 1$.

:::reveal
Yes. The difference quotient at 0 is $\frac{h|h|}{h} = |h|$, which tends to 0 from both sides. The product rule cannot be used here, since $|x|$ has no derivative at 0, but the definition settles it directly. "Contains a corner" is not the same as "has a corner".
:::
::::

## 5. Exponential, logarithm, sine

From M06's series $e^h = 1 + h + h^2/2 + \dots$, the quotient $\frac{e^h - 1}{h} = 1 + h/2 + \dots \to 1$. So

$$
\frac{e^{a + h} - e^a}{h} = e^a \cdot \frac{e^h - 1}{h} \to e^a :
$$

the exponential is its own derivative. The logarithm is its inverse: differentiating $e^{\ln x} = x$ with the chain rule gives $e^{\ln x} \cdot (\ln x)' = 1$, so $(\ln x)' = 1/x$. For the sine, $\sin(a + h) = \sin a \cos h + \cos a \sin h$ (M07), and with $\frac{\sin h}{h} \to 1$ and $\frac{\cos h - 1}{h} \to 0$, $(\sin x)' = \cos x$.

::::derivation{id=d4 title="Derivatives of exponentials and logarithms"}
:::step
By the chain rule, the derivative of $e^{3x}$ is [[3*e^(3*x)]].
:::
:::step
The derivative of $\ln(x^2 + 1)$ is [[2*x/(x^2+1)]].
:::
::::

## 6. One-sided derivatives and subgradients

At a corner the limits from the left and from the right exist but differ. For $|x|$ at 0 they are $-1$ and $1$; for the ReLU, 0 and 1. There is no derivative. For a convex function like these, any slope between the two one-sided ones gives a line that touches the graph at the corner and stays below it: a **subgradient** (M28 builds on it). Frameworks pick one: PyTorch uses 0 for the ReLU at exactly 0. Since an input is almost never exactly 0 in floating point, the choice rarely matters.

## 7. Finite differences and floating point

The derivative is a limit, so approximate it with a small $h$: the **forward difference** $\frac{f(x + h) - f(x)}{h}$ or the **central difference** $\frac{f(x + h) - f(x - h)}{2h}$. Two errors compete.

- **Truncation**: by the next term of the approximation (M16), the forward difference is off by about $\frac{h}{2}|f''|$, the central one by about $\frac{h^2}{6}|f'''|$.
- **Rounding**: $f(x + h)$ and $f(x)$ are each computed with a relative error of about $\varepsilon \approx 2.2 \times 10^{-16}$ (M07), so their difference carries an error of about $\varepsilon|f|$, and dividing by $h$ makes it $\varepsilon|f|/h$.

The total, $\frac{h}{2}|f''| + \frac{\varepsilon |f|}{h}$, is smallest when the two are balanced, at $h^\ast = \sqrt{2\varepsilon|f|/|f''|}$: for ordinary functions about $10^{-8}$, giving about 8 correct digits. For the central difference $h^\ast \approx (3\varepsilon|f|/|f'''|)^{1/3} \approx 10^{-5}$, giving about 10 or 11.

::::derivation{id=d5 title="The best step"}
:::step
For $f = e^x$ at $x = 1$, every derivative equals $e$, so the forward optimum is $h^\ast = \sqrt{2\varepsilon} \approx$ [[2.1e-8|tol=1e-9]].
:::
:::step
At $h^\ast$ the two errors are equal, each about $\frac{h^\ast}{2} e$, so the total error is about $h^\ast e \approx 5.7 \times 10^{-8}$: of the 16 digits of $f$, the derivative keeps about [[7|tol=1]].
:::
::::

:::edge{to=M16 text="the next term of the approximation: Taylor polynomials, extrema and Newton's method."}
:::

:::edge{to=M17 text="the inverse operation: accumulating a rate gives the total, by the fundamental theorem of calculus."}
:::

:::edge{to=M26 text="truncation against rounding, measured across numerical methods."}
:::

:::edge{to=M24 text="the law of large numbers is a limit of the same epsilon kind, about averages of samples."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Limit | for every $\varepsilon$ a $\delta$ | define everything below |
| Continuity | $\lim_{x \to a} f(x) = f(a)$ | no jumps |
| Derivative | limit of secant slopes; best linear approximation | rates of change |
| Rules | sum, product, chain, quotient | differentiate compositions |
| $e^x, \ln x, \sin x$ | $e^x$, $1/x$, $\cos x$ | the building blocks of models |
| Corners | one-sided derivatives, subgradients | ReLU, absolute value |
| Finite differences | best $h \approx 10^{-8}$ forward, $10^{-5}$ central | check derivatives numerically |
