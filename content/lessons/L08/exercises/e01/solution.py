def topo_order(parents):
    """All nodes, each after all of its parents. Raise ValueError on a cycle."""
    state, order = {}, []

    def visit(n):
        if state.get(n) == "done":
            return
        if state.get(n) == "active":
            raise ValueError(f"cycle through {n!r}")
        state[n] = "active"
        for p in parents[n]:
            visit(p)
        state[n] = "done"
        order.append(n)

    for n in parents:
        visit(n)
    return order


def ancestors(parents, root):
    """The set of nodes root depends on, including root."""
    seen, stack = set(), [root]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(parents[n])
    return seen
