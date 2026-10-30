def evaluations(n, method):
    """Evaluations for all n partial derivatives."""
    return n + 1 if method == "forward" else 2 * n


def seconds(n, method, eval_seconds):
    """Total time."""
    return float(evaluations(n, method) * eval_seconds)


def days_for_model(params, eval_seconds):
    """Days for one central-difference gradient."""
    return seconds(params, "central", eval_seconds) / 86400
