def post(pi, s, f):
    """Posterior after one positive."""
    return s * pi / (s * pi + f * (1 - pi))


def dpost_dprior(pi, s, f):
    """Derivative of the posterior with respect to the prior."""
    return s * f / (s * pi + f * (1 - pi)) ** 2


def prior_needed(target, s, f):
    """Prior giving the target posterior."""
    o = target / (1 - target) * f / s
    return o / (1 + o)
