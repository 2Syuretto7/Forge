# A reusable gradient checker

You will check dozens of hand-written gradients in this course. Build the tool once.

- `numerical_gradient(f, x, h)`: central differences for every coordinate of a float64 array `x` of any shape. `f` returns a float. Do not modify `x` permanently.
- `relative_error(a, b)`: $\dfrac{\|a - b\|}{\max(\|a\| + \|b\|, 10^{-12})}$, a float.
- `check_gradient(f, grad_f, x, h, tol)`: return `(ok, err)` where `err` is the relative error between `grad_f(x)` and the numerical gradient and `ok` is `err < tol`.

The tests feed your checker a correct and a subtly wrong gradient and require it to tell them apart.

## Hints

1. Loop over `np.ndindex(x.shape)`, perturb one entry, evaluate, and restore it.
2. Work on a copy: `x = np.array(x, dtype=float)`.
3. A relative error is scale-free, so the same tolerance works for tiny and huge gradients.
