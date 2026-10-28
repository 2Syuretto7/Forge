def gpipe_order(p, m):
    """Every stage runs all m forward passes, then all m backward passes in reverse order. Return,
    for each stage, its list of ("F", j) and ("B", j)."""
    raise NotImplementedError


def one_f_one_b_order(p, m):
    """1F1B: stage s first runs min(p - s - 1, m) warm-up forward passes, then alternates one
    forward and one backward while forwards remain, then runs the remaining backwards, all in
    micro-batch order."""
    raise NotImplementedError


def simulate(orders, tf=1.0, tb=2.0):
    """Run the stages' op lists. F of micro-batch j on stage s needs F of j on stage s - 1; B of j
    on stage s needs B of j on stage s + 1 (the last stage needs its own F of j). Each stage runs
    its ops in order, one at a time. Return (finish time of the last op, the largest number of
    micro-batches any stage holds between its F and B)."""
    raise NotImplementedError
