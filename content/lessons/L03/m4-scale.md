# Scale and measure: expressiveness and cost

How much can a hidden layer represent, and what does a backward pass cost? Three exercises answer with numbers.

## Building functions from hinges

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

::::predict{id=p4 kind=numeric answer=11 tol=0}
A one-hidden-layer ReLU network with 10 hidden units takes a single scalar input. What is the largest possible number of linear pieces of the function it computes?

:::reveal
Each unit contributes at most one kink, at $x = -b/w$, so at most 10 kinks and 11 pieces. With two hidden layers the count can grow multiplicatively with depth, which is one argument for depth: deep ReLU networks can represent functions with exponentially many pieces using only polynomially many units.
:::
::::

## Counting FLOPs

:::exercise{ref=e13}
:::

:::edge{to=L04 text="An autograd engine computes these backward passes for any composition of operations."}
:::
