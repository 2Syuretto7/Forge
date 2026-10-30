def hunt(claim, cases):
    """First case where claim is False, or None."""
    for x in cases:
        if not claim(x):
            return x
    return None


def hunt_count(claim, cases):
    """(first counterexample or None, number of cases tried)."""
    tried = 0
    for x in cases:
        tried += 1
        if not claim(x):
            return x, tried
    return None, tried


def hunt_pairs(claim, xs):
    """First pair (a, b) from xs where claim(a, b) is False, or None."""
    for a in xs:
        for b in xs:
            if not claim(a, b):
                return a, b
    return None
