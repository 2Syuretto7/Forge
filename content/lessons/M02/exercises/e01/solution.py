def evaluate(expr, env):
    """Value of expr (number, variable name, or (op, left, right)) with variables from env."""
    if isinstance(expr, str):
        return env[expr]
    if not isinstance(expr, tuple):
        return expr
    op, a, b = expr
    x, y = evaluate(a, env), evaluate(b, env)
    if op == "+":
        return x + y
    if op == "-":
        return x - y
    if op == "*":
        return x * y
    if op == "/":
        return x / y
    if op == "^":
        return x ** y
    raise ValueError(f"unknown operation {op}")


def variables(expr):
    """The set of variable names in expr."""
    if isinstance(expr, str):
        return {expr}
    if not isinstance(expr, tuple):
        return set()
    return variables(expr[1]) | variables(expr[2])
