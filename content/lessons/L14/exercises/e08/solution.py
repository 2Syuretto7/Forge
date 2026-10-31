def gpipe_order(p, m):
    """Every stage runs all m forward passes, then all m backward passes in reverse order. Return,
    for each stage, its list of ("F", j) and ("B", j)."""
    return [[("F", j) for j in range(m)] + [("B", j) for j in reversed(range(m))] for _ in range(p)]


def one_f_one_b_order(p, m):
    """1F1B: stage s first runs min(p - s - 1, m) warm-up forward passes, then alternates one
    forward and one backward while forwards remain, then runs the remaining backwards, all in
    micro-batch order."""
    orders = []
    for s in range(p):
        warm = min(p - s - 1, m)
        ops = [("F", j) for j in range(warm)]
        f, b = warm, 0
        while f < m:
            ops += [("F", f), ("B", b)]
            f += 1
            b += 1
        ops += [("B", j) for j in range(b, m)]
        orders.append(ops)
    return orders


def simulate(orders, tf=1.0, tb=2.0):
    """Run the stages' op lists. F of micro-batch j on stage s needs F of j on stage s - 1; B of j
    on stage s needs B of j on stage s + 1 (the last stage needs its own F of j). Each stage runs
    its ops in order, one at a time. Return (finish time of the last op, the largest number of
    micro-batches any stage holds between its F and B)."""
    p = len(orders)
    done = {}
    clock = [0.0] * p
    pos = [0] * p
    held = [0] * p
    peak = 0
    while any(pos[s] < len(orders[s]) for s in range(p)):
        progressed = False
        for s in range(p):
            if pos[s] == len(orders[s]):
                continue
            kind, j = orders[s][pos[s]]
            dep = (("F", s - 1, j) if s > 0 else None) if kind == "F" else (("B", s + 1, j) if s < p - 1 else ("F", s, j))
            if dep is not None and dep not in done:
                continue
            start = max(clock[s], done[dep] if dep else 0.0)
            clock[s] = start + (tf if kind == "F" else tb)
            done[(kind, s, j)] = clock[s]
            held[s] += 1 if kind == "F" else -1
            peak = max(peak, held[s])
            pos[s] += 1
            progressed = True
        if not progressed:
            raise RuntimeError("deadlock")
    return max(clock), peak
