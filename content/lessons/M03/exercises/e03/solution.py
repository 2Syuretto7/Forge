def for_all(pred, xs):
    """True when pred holds for every x in xs."""
    for x in xs:
        if not pred(x):
            return False
    return True


def exists(pred, xs):
    """True when pred holds for some x in xs."""
    for x in xs:
        if pred(x):
            return True
    return False


def for_all_exists(rel, xs, ys):
    """For every x there is a y with rel(x, y)."""
    return for_all(lambda x: exists(lambda y: rel(x, y), ys), xs)


def exists_for_all(rel, xs, ys):
    """There is a y with rel(x, y) for every x."""
    return exists(lambda y: for_all(lambda x: rel(x, y), xs), ys)
