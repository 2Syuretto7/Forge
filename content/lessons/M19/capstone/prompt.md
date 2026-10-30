# Capstone: an autodiff library for real code

The starter contains `target(x)`: a 20-line function of three variables with arithmetic, powers, a loop, a branch and six elementary functions. Differentiate it exactly, two ways, in one module:

1. A `Dual` class for forward mode (exercise 5) and a `Var` class for reverse mode (exercise 1), each supporting `+`, `-`, `*`, `/` with numbers on either side, unary minus, `**` with a numeric exponent, and comparisons `<` and `>` by value (so the branch works).
2. The functions `exp`, `log`, `sin`, `cos`, `tanh`, `sqrt` that `target` calls, working on a `Dual`, a `Var` or a plain float.
3. `grad_forward(f, x)`: one forward-mode pass per coordinate. `grad_reverse(f, x)`: one forward evaluation with `Var`s and one backward sweep in reverse topological order. Both return NumPy arrays.
4. `fd_grad(f, x, h=1e-6)`: central differences on plain floats, and `check(f, x)`: the larger of the relative errors of the two exact gradients against `fd_grad`.

The tests compare both gradients with a high-accuracy reference to $10^{-9}$ at points on both sides of the branch, require the two modes to agree to $10^{-12}$, and `check` to report agreement below $10^{-8}$.
