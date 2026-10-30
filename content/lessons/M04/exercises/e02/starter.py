def compose(f, g):
    """The machine x -> f(g(x))."""
    raise NotImplementedError


def compose_all(fs):
    """compose_all([f, g, h])(x) == f(g(h(x))); the identity for an empty list."""
    raise NotImplementedError


def commute_points(f, g, xs):
    """The x in xs where f(g(x)) and g(f(x)) agree within 1e-12."""
    raise NotImplementedError
