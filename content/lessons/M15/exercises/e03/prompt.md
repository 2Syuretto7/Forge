# A reusable gradient checker

You will check many hand-written derivatives in this course. Build the tool once, for functions of a whole array of inputs (M18 calls the result the gradient).

- `numerical_gradient(f, x, h=1e-6)`: central differences for every entry of a float64 array `x` of any shape; `f` returns a float. Do not modify `x` permanently.
- `relative_error(a, b)`: $\dfrac{\|a - b\|}{\max(\|a\| + \|b\|, 10^{-12})}$, a float.
- `check_gradient(f, grad_f, x, h=1e-6, tol=1e-5)`: `(ok, err)` with `err` the relative error between `grad_f(x)` and the numerical gradient, and `ok` whether `err < tol`.

The tests feed your checker a correct and a subtly wrong derivative and require it to tell them apart.

## Hints

1. Loop over `np.ndindex(x.shape)`: perturb one entry, evaluate, restore it.
2. Work on a copy: `x = np.array(x, dtype=float)`.
3. A relative error is scale-free, so one tolerance works for tiny and huge derivatives.
