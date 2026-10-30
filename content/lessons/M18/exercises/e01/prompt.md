# Gradients by hand

Write the gradients, as NumPy arrays:

- `grad_f1(v)` for $f_1(x, y) = x^2 y + \sin y$ (provided as `f1`), with `v = [x, y]`.
- `grad_f2(x)` for $f_2(x) = \|x\|^2$, any length.
- `grad_f3(x)` for $f_3(x) = \log\sum_i e^{x_i}$ (log-sum-exp): the softmax $e^{x_i} / \sum_j e^{x_j}$.
- `grad_f4(x, A)` for $f_4(x) = \frac12 x^\top A x$ with a square, not necessarily symmetric, `A`.

The tests run a **gradient check** of each against central differences.

## Hints

1. Differentiate one variable at a time with the others fixed.
2. $\|x\|^2 = \sum x_i^2$.
3. Subtract `max(x)` before exponentiating, for stability; the softmax does not change.
