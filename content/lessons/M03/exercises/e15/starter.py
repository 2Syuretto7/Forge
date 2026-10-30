def forall_exists(rel, n):
    """For every x in range(n) there is a y with (x, y) in rel."""
    raise NotImplementedError


def exists_forall(rel, n):
    """There is a y with (x, y) in rel for every x in range(n)."""
    raise NotImplementedError


def swap_counterexample(n):
    """A relation where forall-exists holds but exists-forall fails (n >= 2)."""
    raise NotImplementedError


def smallest_counterexample():
    """Smallest n with such a relation."""
    raise NotImplementedError
