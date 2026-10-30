# Build: expressions, a checker and solvers

You will build a tiny computer algebra system: expressions stored as trees, an evaluator, a simplifier, and a checker that tests a claimed step at random points. Then the solvers of the derivation, each checked by an invariant.

An expression tree stores $3x + 2$ as nested tuples: `("+", ("*", 3, "x"), 2)`. A tuple's first item is the operation, and the rest are its operands, which are themselves numbers, variable names (strings) or smaller trees. The operations are `"+"`, `"-"`, `"*"`, `"/"` and `"^"` (power).

## Expression trees

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

## Checking a step at random points

:::exercise{ref=e04}
:::

## Solvers

Each solver below is checked by an invariant: plug the answer back in and the equation holds.

:::exercise{ref=e05}
:::

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::
