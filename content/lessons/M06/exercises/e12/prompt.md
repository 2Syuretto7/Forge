# Fitting growth laws

Taking logarithms turns both growth laws into straight lines.

- `fit_exponential(x, y)`: for data near $y = a\, b^x$, fit a straight line to $\ln y$ against $x$ and return `(a, b)`: the intercept gives $\ln a$, the slope $\ln b$.
- `fit_power(x, y)`: for data near $y = c\, x^p$, fit a straight line to $\ln y$ against $\ln x$ and return `(c, p)`.

Use `np.polyfit(u, v, 1)`, which returns `(slope, intercept)` of the least-squares line. The tests use noisy data and check the parameters to a few percent.

## Hints

1. `slope, icept = np.polyfit(x, np.log(y), 1)`.
2. `a = np.exp(icept)`, `b = np.exp(slope)`.
3. For the power law, fit against `np.log(x)`.
