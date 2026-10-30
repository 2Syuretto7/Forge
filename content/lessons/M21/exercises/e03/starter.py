def post(pi, s, f):
    """Posterior after one positive."""
    raise NotImplementedError


def dpost_dprior(pi, s, f):
    """Derivative of the posterior with respect to the prior."""
    raise NotImplementedError


def prior_needed(target, s, f):
    """Prior giving the target posterior."""
    raise NotImplementedError
