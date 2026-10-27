import numpy as np


def bootstrap_diff(ka, na, kb, nb, B=4000, seed=0):
    """Return (pa_star, pb_star): B resampled conversion rates for each arm."""
    raise NotImplementedError


def bayes_draws(ka, na, kb, nb, prior=(1.0, 1.0), draws=100000, seed=0):
    """Return (pa, pb): posterior samples for each arm under independent Beta priors."""
    raise NotImplementedError


def analyze(ka, na, kb, nb):
    """Return dict with diff, ci, prob_b_better, a_ci_boot, a_ci_bayes, bootstrap_says, bayes_says."""
    raise NotImplementedError


REPORT = """
"""
