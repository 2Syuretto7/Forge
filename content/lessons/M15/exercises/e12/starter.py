def evaluations(n, method):
    """Evaluations for all n partial derivatives."""
    raise NotImplementedError


def seconds(n, method, eval_seconds):
    """Total time."""
    raise NotImplementedError


def days_for_model(params, eval_seconds):
    """Days for one central-difference gradient."""
    raise NotImplementedError
