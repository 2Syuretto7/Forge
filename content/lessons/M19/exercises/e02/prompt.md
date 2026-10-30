# Topological order

- `topo_order(out)`: the nodes reachable from `out` through `parents` (a `Var` from e01, provided), each listed after all of its parents, `out` last; each node once, even if it is reachable along many paths.
- `is_valid_order(order)`: whether every node in the list appears after all of its parents that are in the list.
- `count_paths(out, leaf)`: the number of distinct paths from `out` down to `leaf`; the derivative is a sum over exactly these paths.

The tests build a graph in which one input is used ten times, and a "ladder" whose number of paths doubles at every rung: reverse mode still visits each node once, which is why it does not care how many paths there are.

## Hints

1. Depth-first search with a `seen` set keyed by `id`.
2. Record each node's position in a dictionary, then compare positions.
3. Paths satisfy `paths(v) = sum of paths(p)` over parents, with memoization; without memoization the ladder takes exponential time.
