# Capstone: a dual-number autodiff library for real code

The starter contains `target(x)`: a 20-line function of three variables with arithmetic, powers, a loop, a branch, and six different elementary functions. Your library must differentiate it exactly.

Implement in one module:

1. A `Dual` class (reuse exercise 5) and the functions `exp`, `log`, `sin`, `cos`, `tanh`, `sqrt` that `target` calls. They must work on plain floats too, because the tests also evaluate `target` on floats.
2. `grad(f, x)`: the gradient of a scalar function of a list of floats, by forward mode: one pass per coordinate, seeding that coordinate with `eps = 1` and the others with `0`. Return a NumPy array.
3. `fd_grad(f, x, h)`: the central-difference gradient on plain floats.
4. `check(f, x)`: return the relative error $\|g_{\text{dual}} - g_{\text{fd}}\| / (\|g_{\text{dual}}\| + \|g_{\text{fd}}\|)$ with `h = 1e-6`.

The tests compare your gradient with a high-accuracy reference at several points (including both sides of the branch) to $10^{-9}$, and require `check` to report agreement below $10^{-8}$.
