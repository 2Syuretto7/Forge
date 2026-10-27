# Puzzle: the gradient check that fails at tiny steps

You have written a function and its derivative, and you want to check the derivative numerically. The definition of the derivative suggests a recipe: pick a small $h$ and compute

$$
D_h f(x) = \frac{f(x + h) - f(x)}{h}.
$$

Smaller $h$ should mean a better approximation. Try it on $f(x) = e^x$ at $x = 1$, where the true derivative is $e \approx 2.718281828$, in float64.

::::predict{id=p1 kind=choice answer=c}
Which step size gives the most accurate forward-difference estimate of the derivative of $e^x$ at $x = 1$ in float64?

- $h = 10^{-1}$
- $h = 10^{-4}$
- $h = 10^{-8}$
- $h = 10^{-12}$
- $h = 10^{-16}$

:::reveal
$h = 10^{-8}$ wins, with an error of about $7 \times 10^{-9}$. At $h = 10^{-12}$ the error is about $4 \times 10^{-4}$, and at $h = 10^{-16}$ the estimate is $0$ or wildly off, because $1 + 10^{-16}$ rounds to $1$ in float64 and the two function values are identical. Smaller is better only until rounding error takes over.
:::
::::

::::predict{id=p2 kind=sketch answer="1,0.6,0.2,0.05,0.25,0.7,1" xlabel="log10 of step size, from -1 (left) to -16 (right)" ylabel="log error (scaled)"}
Sketch the error of the forward difference as $h$ shrinks from $10^{-1}$ (left) to $10^{-16}$ (right), on log scales. Only the shape matters.

:::reveal
The error falls along a line of slope one (truncation error proportional to $h$), reaches a minimum near $h = 10^{-8}$, then rises along a line of slope minus one (rounding error proportional to $\varepsilon/h$), getting noisy as it climbs. The V shape is the signature of two competing errors. You will reproduce it exactly in Movement 5.
:::
::::

## Why this matters

Gradient checks are how you trust every backward pass you write in this course: dozens of exercises compare an analytic gradient with central differences at a relative error below $10^{-5}$. To trust the check you need to know where its own errors come from, and which step size makes them smallest.

There is also a deeper question underneath. Finite differences need one or two function evaluations per input coordinate: a model with a billion parameters would need a billion evaluations for one gradient. Real training computes the full gradient at a cost of a few function evaluations. The technique that makes that possible, **reverse-mode automatic differentiation**, is the main subject of this lesson.

:::widget{name=ComputationGraph preset=default}
:::

Press "Backward step" in the widget a few times. Each node's gradient is the sum, over the nodes that use it, of the downstream gradient times a local derivative. That rule, applied mechanically, differentiates any program built from differentiable pieces.

## Questions to carry into the derivation

1. What exactly is the error of $D_h f$, and which $h$ minimizes it?
2. What is the derivative of a function from $\mathbb{R}^n$ to $\mathbb{R}^m$, and how does the chain rule look for such functions?
3. Why can a gradient with a billion entries cost only a few function evaluations?
4. Why does a small step against the gradient reduce a function?
