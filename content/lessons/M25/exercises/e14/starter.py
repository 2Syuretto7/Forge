import numpy as np


def mle_p(k, n):
    raise NotImplementedError


def smoothed_p(k, n, alpha=1.0):
    raise NotImplementedError


def heldout_logloss(p, k_test, n_test):
    """Average negative log-likelihood per held-out flip; inf if an observed outcome had probability 0."""
    raise NotImplementedError


def expected_logloss(estimator, p_true, n_train, n_test, trials, seed=0):
    """Average held-out log-loss of estimator(k, n_train) over simulated datasets."""
    raise NotImplementedError
