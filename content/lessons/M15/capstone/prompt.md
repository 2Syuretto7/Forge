# Capstone: a verified differentiator

Expressions are nested tuples as in e01, with more operators: `("x",)`, `("c", v)`, `("+", a, b)`, `("-", a, b)`, `("*", a, b)`, `("/", a, b)`, `("^", a, k)` with a number `k`, and `("sin", a)`, `("cos", a)`, `("exp", a)`, `("log", a)`, `("tanh", a)`. The starter's `FUNCTIONS` holds 30 of them, each with a point to test at.

1. `evaluate(e, x)` and `derivative(e)` for every operator.
2. `budget(e, x, h)`: the expected error of the central difference at step `h`: $\frac{h^2}{6}|f'''(x)| + \frac{\varepsilon |f(x)|}{h}$, with $f'''$ from three applications of your `derivative`, plus $\varepsilon |f'(x)|$ for the rounding of the result itself. Use $\varepsilon$ = `sys.float_info.epsilon`.
3. `best_h(e, x)`: the step minimizing the budget's two main terms, $\left(3\varepsilon|f(x)|/|f'''(x)|\right)^{1/3}$, falling back to $\varepsilon^{1/3}\max(1, |x|)$ when $f'''(x)$ or $f(x)$ is 0, and never below $10^{-3}$ times that fallback.
4. `verify(e, x, d=None)`: compare `evaluate(d, x)` (default `derivative(e)`) with the central difference at `best_h`, and return `(ok, err, allowed)` where `allowed` is 10 times the budget and `ok` means the error is within it.

The tests run all 30 functions, then plant errors in the derivative and require `verify` to catch every one.
