# Derivation: functions, composition, inverses and pieces

## 1. What a function is

A **function** $f: A \to B$ assigns to every element $x$ of its **domain** $A$ exactly one element $f(x)$ of its **codomain** $B$. You met this definition as a set of pairs in M03. Three words in it matter:

- **every** element of the domain gets an output (so $\sqrt{x}$ on the real numbers needs the domain $x \geq 0$);
- **exactly one** output (so "the number whose square is $x$" is not a function: 4 has two square roots);
- the **range** (or image) is the set of outputs that actually occur, which can be smaller than the codomain.

The **graph** of a real function is the set of points $(x, f(x))$ in the plane. "Exactly one output" becomes the vertical line test: every vertical line meets the graph at most once.

## 2. A catalogue of shapes

- **Linear:** $f(x) = ax$. Through the origin; doubling the input doubles the output.
- **Affine:** $f(x) = ax + b$. A straight line with slope $a$ and intercept $b$. (People often call these linear too; the difference matters in M10.)
- **Quadratic:** $f(x) = ax^2 + bx + c$, a parabola. In M02 you completed the square: $a(x + h)^2 + k$.
- **Polynomial:** $f(x) = c_0 + c_1 x + \dots + c_n x^n$.
- **Rational:** a ratio of two polynomials, undefined where the denominator vanishes.
- **Piecewise:** different formulas on different parts of the domain. $|x|$ and $\operatorname{relu}(x)$ are piecewise linear.

**Evaluating a polynomial cheaply.** Writing $c_0 + c_1 x + c_2 x^2 + c_3 x^3 = c_0 + x(c_1 + x(c_2 + x c_3))$ needs only 3 multiplications and 3 additions, instead of computing each power separately. This is **Horner's rule**, and it is how every library evaluates polynomials.

## 3. Composition

The **composition** $f \circ g$ is the function $x \mapsto f(g(x))$: apply $g$, then $f$. Read the symbol right to left, as the order in which the machines act.

::::derivation{id=d1 title="Composition and its order"}
:::step
Let $f(x) = x^2$ and $g(x) = x + 1$. Then $f(g(2)) = f(3) =$ [[9]].
:::
:::step
And $g(f(2)) = g(4) =$ [[5]].
:::
:::step
As a formula, $(f \circ g)(x) =$ [[(x + 1)^2]], while $(g \circ f)(x) = x^2 + 1$.
:::
::::

Composition is **associative**: $f \circ (g \circ h) = (f \circ g) \circ h$, because both mean "apply $h$, then $g$, then $f$". It is not **commutative**: order matters, as the derivation just showed. A neural network layer is a composition (multiply by weights, add a bias, apply a nonlinearity), and a network is a composition of layers.

**Domains compose too.** $x$ is in the domain of $f \circ g$ when $x$ is in the domain of $g$ and $g(x)$ is in the domain of $f$. For $\sqrt{1 - x^2}$, the inner machine accepts every $x$, but the outer one needs $1 - x^2 \geq 0$, so the domain is $-1 \leq x \leq 1$.

## 4. Inverses

A function $f: A \to B$ has an **inverse** $f^{-1}: B \to A$ when running it backwards is well defined: $f^{-1}(f(x)) = x$ for every $x$ in $A$ and $f(f^{-1}(y)) = y$ for every $y$ in $B$. That needs two things:

- **injective:** no two inputs share an output, or "backwards" would have two answers;
- **surjective onto $B$:** every $y$ in $B$ is reached, or "backwards" would have no answer.

To find a formula for the inverse, solve $y = f(x)$ for $x$: inverting is solving the equation of M02 for every right-hand side at once.

::::derivation{id=d2 title="Inverses, and the inverse of a composition"}
:::step
For $f(x) = 3x + 2$, solving $y = 3x + 2$ for $x$ gives $f^{-1}(y) =$ [[(y - 2)/3]].
:::
:::step
To undo "apply $g$, then $f$", undo $f$ first and then $g$: $(f \circ g)^{-1} = g^{-1} \circ f^{-1}$, like taking off shoes before socks. With $g(x) = x + 1$ and $f(x) = 2x$, $(f \circ g)^{-1}(y) =$ [[y/2 - 1]].
:::
:::step
$x^2$ on all real numbers is not injective, since $(-2)^2 = 2^2$. Restricted to $x \geq 0$ it is, and its inverse is the square root. Is $x^3$ injective on all real numbers? Answer yes or no: [[word:yes]].
:::
::::

When no formula for the inverse exists, you can still compute it for an increasing function by **bisection**: to find $x$ with $f(x) = y$, start with an interval $[\text{lo}, \text{hi}]$ where $f(\text{lo}) \leq y \leq f(\text{hi})$, test the midpoint, keep the half that still brackets $y$, and repeat. Each step halves the interval, so 50 steps shrink it by $2^{50} \approx 10^{15}$. You will build this, and M06 uses it to compute logarithms from the exponential.

::::predict{id=p3 kind=choice answer=a}
Bisection is run on $f(x) = x^3$ to find the input with output 10, starting from $[0, 10]$. After 40 steps, how wide is the interval?

- About $10^{-11}$.
- About $10^{-3}$.
- About 0.25.
- It depends on how steep $f$ is.

:::reveal
$10 / 2^{40} \approx 10 / (1.1 \times 10^{12}) \approx 9 \times 10^{-12}$. The width halves every step whatever the function does, which is why bisection is so reliable: it needs only that $f$ is continuous and increasing, never its formula or its slope.
:::
::::

## 5. Transformations are compositions

Moving and stretching a graph is composition with affine machines.

| Change to the graph | New function | Composition |
| --- | --- | --- |
| shift right by $h$ | $f(x - h)$ | $f \circ (x \mapsto x - h)$ |
| shift up by $k$ | $f(x) + k$ | $(y \mapsto y + k) \circ f$ |
| stretch horizontally by $a$ | $f(x / a)$ | $f \circ (x \mapsto x / a)$ |
| stretch vertically by $b$ | $b f(x)$ | $(y \mapsto by) \circ f$ |
| reflect in the $y$ axis | $f(-x)$ | $f \circ (x \mapsto -x)$ |
| reflect in the $x$ axis | $-f(x)$ | $(y \mapsto -y) \circ f$ |

Changes inside, to $x$, act on the horizontal axis and look backwards: shifting right means subtracting $h$, because the new function must reach at $x = h$ the value the old one had at 0.

::::derivation{id=d3 title="Moving a parabola"}
:::step
Shifting $f(x) = x^2$ right by 3 and up by 1 gives [[(x - 3)^2 + 1]].
:::
:::step
That parabola's lowest point is at $x = 3$, where its value is [[1]].
:::
:::step
Reflecting $g(x) = (x - 3)^2 + 1$ in the $y$ axis gives $g(-x) = (-x - 3)^2 + 1$, whose lowest point is at $x =$ [[-3]].
:::
::::

## 6. Drawing curves with ReLU pieces

Now the puzzle. Two shifted ramps make a step and three make a **hat**:

$$
\operatorname{hat}(x) = \operatorname{relu}(x) - 2\,\operatorname{relu}(x - 1) + \operatorname{relu}(x - 2) .
$$

It is 0 for $x \leq 0$, rises to 1 at $x = 1$, falls back to 0 at $x = 2$, and stays 0 after: each ReLU changes the slope by its coefficient at its own corner (slopes $0 \to 1 \to -1 \to 0$).

Any **piecewise-linear** function with corners at $t_1 < t_2 < \dots$ is a sum of shifted ReLUs, for the same reason: start with a straight line, and at each corner $t_k$ add $w_k \operatorname{relu}(x - t_k)$, where $w_k$ is the change of slope there. To draw a curve $f$, put corners on the curve at equally spaced points $t_0, \dots, t_n$ and join them with straight pieces.

How good is that drawing? On one piece of length $h$, the straight chord and the curve agree at both ends. If the curve bends with curvature (second derivative, coming in M15) at most $M$, the gap between curve and chord is at most

$$
\frac{h^2}{8} M .
$$

You can see where the $h^2$ comes from with $f(x) = x^2$, whose bending is the same everywhere ($M = 2$): on the piece $[0, h]$ the chord is $y = hx$, and the gap $hx - x^2$ is largest at the midpoint $x = h/2$.

::::derivation{id=d4 title="Why halving the pieces quarters the error"}
:::step
At $x = h/2$ the gap $hx - x^2$ equals $h \cdot \frac{h}{2} - \frac{h^2}{4} =$ [[h^2/4]], which is $\frac{h^2}{8} M$ with $M = 2$.
:::
:::step
So halving $h$ divides the error by [[4]].
:::
:::step
The hill $e^{-x^2}$ bends at most $M = 2$ (at its top). On $[-3, 3]$ with $n$ pieces, $h = 6/n$, so the error is about $\frac{(6/n)^2}{8} \cdot 2 = \frac{9}{n^2}$. For an error of 0.01 you need $n$ about [[30]].
:::
::::

:::edge{to=L03 text="a sum of shifted ReLUs is exactly a neural network with one hidden layer; in L03 training chooses the corners and the slopes instead of you."}
:::

The same picture explains why bigger networks fit better, and also why a curve with a sharp feature needs many pieces near it: the error bound depends on how hard the curve bends, and a curve that bends without limit (like $\sqrt{x}$ at 0) breaks the $h^2$ law, as you will find in Movement 5.

:::widget{name=FunctionMachine mode=compose f=square g=plus1}
:::

:::edge{to=M06 text="the exponential and the logarithm are a function and its inverse, and bisection computes one from the other."}
:::

:::edge{to=M09 text="a function can output a list of numbers instead of one: a vector-valued function."}
:::

## Summary

| Idea | Statement | Watch out for |
| --- | --- | --- |
| Function | each input in the domain gets exactly one output | the domain is part of the function |
| Composition | $(f \circ g)(x) = f(g(x))$, associative | not commutative |
| Inverse | exists when the function is injective and onto | $(f \circ g)^{-1} = g^{-1} \circ f^{-1}$ |
| Transformations | composition with affine maps | inside changes run backwards |
| ReLU pieces | any piecewise-linear function is a sum of shifted ReLUs | error $\frac{h^2}{8} M$ needs bounded bending |
