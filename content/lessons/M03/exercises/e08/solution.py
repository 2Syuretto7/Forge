def failures(p, q, cases):
    """Cases where p(x) implies q(x) fails."""
    return [x for x in cases if p(x) and not q(x)]


def contrapositive_failures(p, q, cases):
    """Cases where not q(x) implies not p(x) fails."""
    return [x for x in cases if (not q(x)) and not (not p(x))]


def converse_failures(p, q, cases):
    """Cases where q(x) implies p(x) fails."""
    return failures(q, p, cases)
