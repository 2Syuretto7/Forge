def to_string(expr):
    """Fully parenthesized text of expr."""
    raise NotImplementedError


def count_operations(expr):
    """Number of operations (tuples) in expr."""
    raise NotImplementedError


def depth(expr):
    """Longest chain of nested operations; 0 for a number or name."""
    raise NotImplementedError
