def to_string(expr):
    """Fully parenthesized text of expr."""
    if isinstance(expr, tuple):
        op, a, b = expr
        return f"({to_string(a)} {op} {to_string(b)})"
    return str(expr)


def count_operations(expr):
    """Number of operations (tuples) in expr."""
    if isinstance(expr, tuple):
        return 1 + count_operations(expr[1]) + count_operations(expr[2])
    return 0


def depth(expr):
    """Longest chain of nested operations; 0 for a number or name."""
    if isinstance(expr, tuple):
        return 1 + max(depth(expr[1]), depth(expr[2]))
    return 0
