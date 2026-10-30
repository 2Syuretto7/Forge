# Capstone: a one-dimensional optimizer suite

Three minimizers (gradient descent, the secant method on $f'$, and Newton's method) run on the same test problems, and each reports the errors of its iterates. Your suite measures the convergence order and rate from those errors and must match theory within 10 percent: order 1 with rate $|1 - \eta f''(x^\ast)|$ for gradient descent, order about 1.618 for the secant method, order 2 for Newton.

:::exercise{ref=capstone}
:::

## When you finish

You know three speeds of convergence and how to measure them. M18 takes Taylor's theorem to many variables, where the second derivative becomes the Hessian; M29 proves the rates of gradient descent and momentum in any dimension, where the ratio of the largest to the smallest curvature, the condition number, sets the speed.

:::edge{to=M29 text="convergence rates of gradient methods, proved in any dimension."}
:::
