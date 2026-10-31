import numpy as np


def _loss(w, X, y):
    raise NotImplementedError


def sgd(X, y, w0, step, iters, batch, rng):
    """Minibatch SGD on least squares: (final w, losses every 10 steps)."""
    raise NotImplementedError


def excess_floor(X, y, step, batch, rng, iters=4000):
    """Average excess loss over the second half of a run started at the optimum."""
    raise NotImplementedError
