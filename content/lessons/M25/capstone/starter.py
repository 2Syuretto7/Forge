import numpy as np


def bootstrap_diff(ka, na, kb, nb, B=4000, seed=0):
    """Return (pa_star, pb_star): B resampled conversion rates for each arm."""
    raise NotImplementedError


def bayes_draws(ka, na, kb, nb, prior=(1.0, 1.0), draws=100000, seed=0):
    """Return (pa, pb): posterior samples for each arm under independent Beta priors."""
    raise NotImplementedError


def _interval(v):
    raise NotImplementedError


def analyze(ka, na, kb, nb):
    """Return dict with diff, ci, prob_b_better, a_ci_boot, a_ci_bayes, bootstrap_says, bayes_says."""
    raise NotImplementedError


REPORT = """
With a large test (200 of 2000 against 260 of 2000) both methods agree that B is better: the
bootstrap interval for the difference sits well above zero and the posterior probability that
B is better is above 0.99. With plenty of data the prior hardly matters and the resampling
distribution is close to the true sampling distribution, so the answers match.
When arm A has zero conversions out of 15 against 4 of 15 for B, both verdicts say B, but the
bootstrap claims to know p_A exactly: resampling an arm of all zeros always returns zero, so its
interval for p_A has zero width. The posterior under a uniform prior keeps p_A uncertain, with
an interval up to about 0.2. In the small test (2 of 20 against 7 of 20) they disagree: with so
few outcomes the bootstrap differences take only a few distinct values, a lump of them sits
exactly at zero, and the lower end of the interval lands on zero, so the bootstrap says
unclear while the posterior probability of about 0.97 says B. Small samples make the bootstrap
lumpy and overconfident at the boundaries, while the prior adds a pseudo-observation that
smooths the answer. In the moderate test both say unclear and their numbers agree.
"""
