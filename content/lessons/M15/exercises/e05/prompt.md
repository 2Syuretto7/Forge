# The rules as functions

Each argument is a function of one variable; `df` and `dg` are their derivatives.

- `product_rule(f, df, g, dg)`: the derivative of $x \mapsto f(x)g(x)$, as a function.
- `quotient_rule(f, df, g, dg)`: the derivative of $f/g$: $(f'g - fg')/g^2$.
- `chain_rule(f, df, g, dg)`: the derivative of $x \mapsto f(g(x))$: $f'(g(x))\,g'(x)$.

The tests check each against central differences at random points (a **gradient check**) for several pairs of functions.

## Hints

1. Return a `lambda x: ...`.
2. Evaluate `g(x)` once inside the chain rule.
3. Keep the quotient rule's sign straight: $f'g - fg'$.
