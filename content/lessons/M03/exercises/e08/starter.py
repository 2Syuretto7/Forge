def failures(p, q, cases):
    """Cases where p(x) implies q(x) fails."""
    raise NotImplementedError


def contrapositive_failures(p, q, cases):
    """Cases where not q(x) implies not p(x) fails."""
    raise NotImplementedError


def converse_failures(p, q, cases):
    """Cases where q(x) implies p(x) fails."""
    raise NotImplementedError
