# The wrong order

The starter provides `Var` (with `+`, `*` and `sin`).

- `backward_in(out, order)`: run the backward pass, processing nodes in the given list from first to last (each node passes `node.grad * local` to its parents), starting from `out.grad = 1`.
- `bfs_order(out)`: breadth-first from `out` through `parents`, each node once, in the order first reached: a plausible but wrong processing order.
- `reverse_topo_order(out)`: the correct one, the reverse of a depth-first postorder.

On a graph where an intermediate value feeds both a short path and a long path to the output, breadth-first order processes that value before the long path has delivered its contribution, passes on an incomplete adjoint, and the input's gradient comes out wrong, silently. (An input has no parents, so processing it early is harmless; the damage is done by intermediate nodes.)

## Hints

1. A queue: `collections.deque`; mark nodes when first enqueued.
2. Reset every node's `grad` to 0 before each backward pass you compare.
3. The test graph: $z = x \cdot w$, then $f = \sin(\sin(\sin(z))) + z \cdot y$.
