# A derivative checker with scaled steps

- `scaled_step(x, kind)`: a step proportional to the size of $x$: $h = \sqrt{\varepsilon}\,|x|$ for `"forward"` and $h = \varepsilon^{1/3}|x|$ for `"central"` (with $|x|$ replaced by 1 at $x = 0$), where $\varepsilon$ = `sys.float_info.epsilon`.
- `check_derivative(f, df, xs, tol=1e-6)`: for each `x` in `xs`, the relative error $|d - c| / \max(|d|, |c|, 10^{-12})$ between `df(x)` and the central difference at `scaled_step(x, "central")`; return the list of `(x, err)` pairs with `err > tol` (empty when all pass).

The tests check a correct derivative of $\log$ over inputs from $10^{-3}$ to $10^{8}$, where a fixed step fails at both ends, and catch a derivative with a typo.

## Hints

1. A step proportional to $x$ keeps $x + h$ distinguishable from $x$ when $x$ is large, and keeps $h$ small compared with $x$ when $x$ is small, where $\log$ curves sharply: at $x = 10^{-3}$ a step of $6 \times 10^{-6}$ is already too coarse.
2. `sys.float_info.epsilon` is $2.2 \times 10^{-16}$.
3. Return an empty list for a correct derivative.
