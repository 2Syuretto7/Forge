# Recall bridge: derivatives you already know

This lesson has no prerequisite lessons. The bridge checks the single-variable calculus it builds on. If earlier lessons have reviews due, they appear above; M10's matrix products show up again in Section 6 of the derivation.

## The derivative as a rate and as a slope

The derivative $f'(x) = \lim_{h \to 0} \dfrac{f(x + h) - f(x)}{h}$ is the slope of the tangent line. Near $x$, the function is close to that line: $f(x + h) \approx f(x) + f'(x)\,h$. This lesson upgrades both readings to many variables, where the slope becomes a matrix.

## Rules you will use without thinking

| Function | Derivative |
| --- | --- |
| $x^n$ | $n x^{n-1}$ |
| $e^x$ | $e^x$ |
| $\log x$ | $1/x$ |
| $\sin x$ | $\cos x$ |
| $\tanh x$ | $1 - \tanh^2 x$ |
| $f(g(x))$ | $f'(g(x))\, g'(x)$ |

::::derivation{id=d0 title="Warm-up derivatives"}
:::step
The derivative of $x^3$ at $x = 2$ is [[12]].
:::
:::step
By the chain rule, the derivative of $e^{3x}$ is [[3*exp(3*x)]].
:::
:::step
The derivative of $\log(1 + x^2)$ is [[2*x/(1 + x^2)]].
:::
:::step
The sigmoid $\sigma(x) = 1/(1 + e^{-x})$ has derivative $\sigma(x)(1 - \sigma(x))$. At $x = 0$ that equals [[0.25]].
:::
::::

Keep the sigmoid fact: in L05 and L07 it makes the gradient of logistic regression collapse to a single subtraction.
