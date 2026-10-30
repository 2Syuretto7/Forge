def evaluate(expr, env):
    """Value of expr (number, variable name, or (op, left, right)) with variables from env."""
    raise NotImplementedError


def variables(expr):
    """The set of variable names in expr."""
    raise NotImplementedError
