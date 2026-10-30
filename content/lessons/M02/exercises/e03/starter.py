NUM = (int, float)


def _apply(op, x, y):
    raise NotImplementedError


def simplify(expr):
    """Apply constant folding and the identity rules, bottom-up."""
    raise NotImplementedError
