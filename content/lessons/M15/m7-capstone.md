# Capstone: a verified differentiator

Write a symbolic differentiator for expression trees (sums, products, quotients, powers, $\sin$, $\cos$, $\exp$, $\log$ and $\tanh$, with the chain rule), and verify it on 30 functions. For each, compute the derivative symbolically, the third derivative too, and compare the first derivative with a central difference at the optimal step for that function and point. The comparison passes only within an error budget computed from the third derivative and the machine epsilon: a check that knows how accurate it can be.

:::exercise{ref=capstone}
:::

## When you finish

You have a differentiator and the means to trust it. M16 uses the second derivative for Taylor polynomials, extrema and Newton's method; M18 takes derivatives of functions of many variables; M19 replaces symbolic differentiation with automatic differentiation, which computes exact derivatives of programs without expression swell.

:::edge{to=M16 text="second derivatives: Taylor polynomials, the second-derivative test and Newton's method."}
:::
