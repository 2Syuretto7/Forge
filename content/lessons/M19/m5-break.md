# Break it: forgotten accumulation and a wrong order

## Reuse a node and overwrite its gradient

:::exercise{ref=e14}
:::

## Visit the nodes in the wrong order

::::predict{id=p5 kind=choice answer=c}
A reverse-mode engine visits a node before all the nodes that use it have sent their contributions. What happens?

- Nothing: the order does not matter for sums.
- It crashes.
- That node passes on an incomplete adjoint, and every input upstream of it gets a wrong gradient, silently.
- Only that node's own gradient is wrong.

:::reveal
The node's adjoint is still missing some terms when it is propagated, and the error flows to everything upstream. A topological order guarantees that every consumer has finished before a node is processed. Engines build it with a depth-first search over the graph, then walk it in reverse.
:::
::::

:::exercise{ref=e15}
:::

The graph uses $x$ twice, once in $a = xy$ and once in $b = \sin x$. Step backward and check that $x$'s gradient collects both paths.

:::widget{name=ComputationGraph preset=default}
:::

## What to take away

- Accumulate adjoints with a sum; zero them before each new backward pass.
- Process nodes in reverse topological order.
- Test every engine against finite differences on functions that reuse values and branch.
