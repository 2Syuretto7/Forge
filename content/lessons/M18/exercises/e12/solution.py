def fd_evaluations(n):
    """Central differences for n inputs."""
    return 2 * n


def fd_seconds(n, eval_seconds):
    """Time of a central-difference gradient."""
    return fd_evaluations(n) * eval_seconds


def directional_evaluations(k):
    """Random-direction check with k directions."""
    return 2 * k


def analytic_ratio(cost_grad, cost_f):
    """Gradient cost in units of evaluations."""
    return cost_grad / cost_f
