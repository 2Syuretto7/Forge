# Monte Carlo integration with an error bar

To integrate $f$ over $[a, b]$, draw $U_i$ uniform on $[a, b]$ and average $(b - a)f(U_i)$ (Section 4). The average is unbiased, and its standard error is the sample standard deviation of the terms over $\sqrt n$.

- `mc_integrate(f, a, b, n, rng)`: return `(estimate, standard_error)`, drawing the points with one call `rng.random(n)`.

The tests integrate $x^2$ and the quarter circle, require each estimate within 4 standard errors of the truth, and check that four times the samples halve the error bar.

## Hints

1. `u = a + (b - a) * rng.random(n)`, then `v = (b - a) * f(u)`.
2. `v.std(ddof=1) / np.sqrt(n)`.
3. The standard error is itself estimated from the samples; at $n = 1000$ it is good to a few percent.
