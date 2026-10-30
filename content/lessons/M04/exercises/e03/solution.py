import math


def with_domain(f, ok, name):
    """A machine computing f(x) when ok(x), else raising ValueError."""
    def machine(x):
        if not ok(x):
            raise ValueError(f"{name}: {x} is outside the domain")
        return f(x)
    return machine


safe_sqrt = with_domain(math.sqrt, lambda x: x >= 0, "sqrt")
safe_log = with_domain(math.log, lambda x: x > 0, "log")
safe_reciprocal = with_domain(lambda x: 1 / x, lambda x: x != 0, "reciprocal")


def in_composite_domain(f_ok, g, g_ok, x):
    """Whether x is in the domain of f after g."""
    return g_ok(x) and f_ok(g(x))
