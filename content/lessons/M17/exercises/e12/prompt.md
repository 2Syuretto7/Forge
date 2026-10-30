# Predicting the cost

A rule with error $C h^p$ on an interval of length 1 needs $h \leq (\text{tol}/C)^{1/p}$.

- `strips_needed(C, p, tol)`: $\lceil (C/\text{tol})^{1/p} \rceil$ strips.
- `trapezoid_constant(max_f2, length)`: $C = \text{length}^3 \max|f''| / 12$ divided by $\text{length}^2$, so that the error is $C h^2$ with $h$ the strip width... simplified: the error of the trapezoid rule on $[a, b]$ with $n$ strips is about $\frac{(b - a)^3}{12 n^2}\max|f''|$; return the strips for a tolerance: `trapezoid_strips(max_f2, length, tol)`.
- `simpson_strips(max_f4, length, tol)`: the same with $\frac{(b - a)^5}{180 n^4}\max|f''''|$, rounded up to an even number.

For $\int_0^\pi \sin x$ to $10^{-8}$: about 16,000 trapezoid strips and about 116 Simpson strips.

## Hints

1. Solve the error formula for $n$.
2. `math.ceil`, then add 1 if odd for Simpson.
3. For $\sin$, both derivative bounds are 1.
