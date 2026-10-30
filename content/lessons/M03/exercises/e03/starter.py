def for_all(pred, xs):
    """True when pred holds for every x in xs."""
    raise NotImplementedError


def exists(pred, xs):
    """True when pred holds for some x in xs."""
    raise NotImplementedError


def for_all_exists(rel, xs, ys):
    """For every x there is a y with rel(x, y)."""
    raise NotImplementedError


def exists_for_all(rel, xs, ys):
    """There is a y with rel(x, y) for every x."""
    raise NotImplementedError
