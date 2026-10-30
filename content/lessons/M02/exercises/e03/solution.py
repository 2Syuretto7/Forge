NUM = (int, float)


def _apply(op, x, y):
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    if op == "/":
        return x / y
    return x ** y


def simplify(expr):
    """Apply constant folding and the identity rules, bottom-up."""
    if not isinstance(expr, tuple):
        return expr
    op, a, b = expr
    a, b = simplify(a), simplify(b)
    if isinstance(a, NUM) and isinstance(b, NUM) and not (op == "/" and b == 0):
        return _apply(op, a, b)
    if op == "+":
        if b == 0:
            return a
        if a == 0:
            return b
    if op == "-":
        if b == 0:
            return a
        if a == b:
            return 0
    if op == "*":
        if b == 1:
            return a
        if a == 1:
            return b
        if a == 0 or b == 0:
            return 0
    if op == "/" and b == 1:
        return a
    if op == "^":
        if b == 1:
            return a
        if b == 0:
            return 1
    return (op, a, b)
