import numpy as np


def bootstrap_diff(ka, na, kb, nb, B=4000, seed=0):
    """Return (pa_star, pb_star): B resampled conversion rates for each arm."""
    rng = np.random.default_rng(seed)
    a = np.concatenate([np.ones(ka), np.zeros(na - ka)])
    b = np.concatenate([np.ones(kb), np.zeros(nb - kb)])
    ia = rng.integers(0, na, size=(B, na))
    ib = rng.integers(0, nb, size=(B, nb))
    return a[ia].mean(axis=1), b[ib].mean(axis=1)


def bayes_draws(ka, na, kb, nb, prior=(1.0, 1.0), draws=100000, seed=0):
    """Return (pa, pb): posterior samples for each arm under independent Beta priors."""
    a0, b0 = prior
    rng = np.random.default_rng(seed)
    pa = rng.beta(a0 + ka, b0 + na - ka, size=draws)
    pb = rng.beta(a0 + kb, b0 + nb - kb, size=draws)
    return pa, pb


def _interval(v):
    lo, hi = np.quantile(v, [0.025, 0.975])
    return float(lo), float(hi)


def analyze(ka, na, kb, nb):
    """Return dict with diff, ci, prob_b_better, a_ci_boot, a_ci_bayes, bootstrap_says, bayes_says."""
    sa, sb = bootstrap_diff(ka, na, kb, nb, 4000, 0)
    pa, pb = bayes_draws(ka, na, kb, nb, (1.0, 1.0), 100000, 0)
    lo, hi = _interval(sb - sa)
    p = float(np.mean(pb > pa))
    return {
        "diff": kb / nb - ka / na,
        "ci": (lo, hi),
        "prob_b_better": p,
        "a_ci_boot": _interval(sa),
        "a_ci_bayes": _interval(pa),
        "bootstrap_says": "B" if lo > 0 else "A" if hi < 0 else "unclear",
        "bayes_says": "B" if p > 0.95 else "A" if p < 0.05 else "unclear",
    }


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
