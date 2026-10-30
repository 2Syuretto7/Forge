def compose(f, g):
    """The machine x -> f(g(x))."""
    return lambda x: f(g(x))


def compose_all(fs):
    """compose_all([f, g, h])(x) == f(g(h(x))); the identity for an empty list."""
    def machine(x):
        for f in reversed(fs):
            x = f(x)
        return x
    return machine


def commute_points(f, g, xs):
    """The x in xs where f(g(x)) and g(f(x)) agree within 1e-12."""
    return [x for x in xs if abs(f(g(x)) - g(f(x))) <= 1e-12]
