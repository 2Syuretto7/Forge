# Gradient descent on a quadratic

1. `quad_fg(A, b, x)` returns the value and gradient of $f(x) = \tfrac12 x^\top A x - b^\top x$ for a symmetric matrix $A$.
2. `gd(grad, x0, lr, steps)` runs gradient descent $x \leftarrow x - \eta\, \nabla f(x)$ from `x0`, where `grad` is a function returning the gradient, and returns every iterate as an array of shape `(steps + 1, d)`, starting with `x0`.

The minimizer of $f$ solves $Ax = b$; the tests check that your iteration finds it.

## Hints

1. The gradient of $\tfrac12 x^\top A x$ is $Ax$ when $A$ is symmetric.
2. Copy `x0` into a float array before iterating, so the caller's array is never modified.
3. Collect the iterates in a list and convert with `np.array` at the end.
