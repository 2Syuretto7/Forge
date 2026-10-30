# A thousand integrals to 1e-8

The family $f(x) = e^{-ax}\cos(bx)$ on $[0, 1]$ has the exact integral $\frac{a - e^{-a}(a\cos b - b\sin b)}{a^2 + b^2}$.

- `exact(a, b)`: that value.
- `evals_doubling(rule, f, tol, exact_value)`: starting from 2 strips, double the strips until the rule's error is below `tol`; return the number of function evaluations of the last call (strips plus one).
- `survey(n_funcs=1000, seed=0)`: draw $a \in [0, 5]$ and $b \in [0, 30]$ uniformly; for each function count the evaluations of the trapezoid rule, Simpson's rule (both by doubling) and adaptive Simpson (provided, with tolerance $10^{-9}$), and return the three averages.

Simpson needs a few hundred evaluations, the trapezoid rule thousands, and adaptive Simpson, which does not know the answer, about as many as Simpson does.

## Hints

1. `rule(f, 0, 1, n)` with `n` doubled each round.
2. Trapezoid and Simpson as in e01 and e02, vectorized.
3. Counting with knowledge of the exact value is a benchmark, not a method; adaptive Simpson estimates its error itself.
