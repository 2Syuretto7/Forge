# Break it: the step-size sweep

Reproduce the V-shaped error curve of the puzzle and find its minimum.

- `sweep(f, df, x, hs, method)`: for each step in the array `hs`, the absolute error of the `"forward"` or `"central"` estimate. Return an array the same shape as `hs`.
- `best_step(hs, errors)`: the step with the smallest error.
- `predicted_best_step(fx, f2, eps, method)`: the theoretical optimum from Section 1. For `"forward"`, $\sqrt{b/a}$ with $a = |f''|/2$ and $b = \varepsilon|f|$; for `"central"`, $(b/(2c))^{1/3}$ with $c = |f'''|/6$ and `f2` meaning $f'''$ in that case.

The tests sweep $h$ from $10^{-1}$ to $10^{-15}$ for $e^x$ at $x = 1$ and check that the measured minimum lands within a factor of 30 of your prediction.

## Hints

1. `np.array([abs(est(h) - df(x)) for h in hs])`.
2. `hs[np.argmin(errors)]`.
3. For $e^x$ every derivative equals $e^x$, so `fx` and `f2` are both $e$; take $\varepsilon = 2.2 \times 10^{-16}$.
