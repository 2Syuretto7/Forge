# Differentiating expression trees

An expression is a nested tuple: `("x",)`, `("c", 2.5)`, `("+", a, b)`, `("*", a, b)`, `("^", a, k)` with a number `k`, `("sin", a)`, `("cos", a)`, `("exp", a)`.

- `evaluate(e, x)`: the value at the number `x`.
- `derivative(e)`: a new tree for the derivative, using the sum, product, power and chain rules: the derivative of $u^k$ is $k u^{k-1} u'$, of $\sin u$ is $\cos u \cdot u'$, and so on.
- `size(e)`: the number of nodes, to watch the derivative trees grow.

The tests check the derivatives against central differences at random points (a **gradient check**).

## Hints

1. Recursion on the first element of the tuple.
2. The product rule: `("+", ("*", da, b), ("*", a, db))`.
3. No simplification is needed; correctness first.
