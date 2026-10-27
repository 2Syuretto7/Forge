# Topological order and cycle detection

A computation graph is given as a dictionary `parents` mapping each node name to the list of its parents (the nodes it was computed from). Every node appears as a key.

- `topo_order(parents)` returns a list of all nodes in which every node comes after all of its parents. If the graph has a directed cycle, raise `ValueError`.
- `ancestors(parents, root)` returns the set of nodes `root` depends on, including `root` itself: exactly the nodes a backward pass from `root` must visit.

## Hints

1. Depth-first search: visit a node's parents first, then append the node. Track three states per node: unvisited, in progress, done.
2. Meeting a node that is still in progress means you followed a cycle back to it.
3. For `ancestors`, walk parents from `root` with a stack and a visited set.
