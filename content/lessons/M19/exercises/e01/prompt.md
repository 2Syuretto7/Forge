# A scalar reverse-mode engine

Write `Var`, a number that remembers how it was computed:

- `Var(value, parents=())` stores `value`, `grad = 0.0`, and `parents`, a tuple of `(var, local_derivative)` pairs.
- Operators `+`, `-`, `*`, `/` (with `Var`s or plain numbers on either side), unary minus, and `**` with a numeric exponent, each creating a new `Var` with the right local derivatives.
- Functions `exp`, `log`, `sin`, `tanh` that accept a `Var`.
- `backward(out)`: set `out.grad = 1`, order the graph so that every node comes after all the nodes that use it (a reverse topological order from a depth-first search), and for each node add `node.grad * local` to each parent's `grad`.

The tests run a **gradient check** against central differences on functions that reuse values.

## Hints

1. `a * b` has parents `((a, b.value), (b, a.value))`.
2. Depth-first search: visit parents first, then append the node; reverse the list.
3. Accumulate with `+=`: a value used twice receives two contributions.
