def forall_exists(rel, n):
    """For every x in range(n) there is a y with (x, y) in rel."""
    return all(any((x, y) in rel for y in range(n)) for x in range(n))


def exists_forall(rel, n):
    """There is a y with (x, y) in rel for every x in range(n)."""
    return any(all((x, y) in rel for x in range(n)) for y in range(n))


def swap_counterexample(n):
    """A relation where forall-exists holds but exists-forall fails (n >= 2)."""
    return {(x, x) for x in range(n)}


def smallest_counterexample():
    """Smallest n with such a relation."""
    return 2
