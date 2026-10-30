def fd_evaluations(n):
    """Central differences for n inputs."""
    raise NotImplementedError


def fd_seconds(n, eval_seconds):
    """Time of a central-difference gradient."""
    raise NotImplementedError


def directional_evaluations(k):
    """Random-direction check with k directions."""
    raise NotImplementedError


def analytic_ratio(cost_grad, cost_f):
    """Gradient cost in units of evaluations."""
    raise NotImplementedError
