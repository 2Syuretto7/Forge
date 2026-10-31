import math
import numpy as np
import sub


def test_bootstrap_rates_large_test():
    sa, sb = sub.bootstrap_diff(200, 2000, 260, 2000, 4000, 0)
    assert sa.shape == (4000,) and sb.shape == (4000,)
    d = sb - sa
    lo, hi = np.quantile(d, [0.025, 0.975])
    se = np.sqrt(0.1 * 0.9 / 2000 + 0.13 * 0.87 / 2000)
    assert lo < 0.03 < hi
    assert abs((hi - lo) / (2 * 1.96 * se) - 1) < 0.1


def test_posterior_probability_matches_integration():
    pa, pb = sub.bayes_draws(3, 10, 6, 10, (1.0, 1.0), 200000, 0)
    p = np.mean(pb > pa)
    t = (np.arange(4000) + 0.5) / 4000

    def pdf(a, b):
        return np.exp((a - 1) * np.log(t) + (b - 1) * np.log1p(-t) - (math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)))

    fa, fb = pdf(4, 8), pdf(7, 5)
    Fa = np.cumsum(fa) / 4000 - 0.5 * fa / 4000
    assert abs(p - np.sum(fb * Fa) / 4000) < 0.006


def test_clear_effect_both_say_b():
    out = sub.analyze(200, 2000, 260, 2000)
    assert out["bootstrap_says"] == "B" and out["bayes_says"] == "B"
    assert abs(out["diff"] - 0.03) < 1e-12


def test_zero_conversion_arm():
    out = sub.analyze(0, 15, 4, 15)
    assert out["a_ci_boot"] == (0.0, 0.0), "resampling all zeros gives zero every time"
    lo, hi = out["a_ci_bayes"]
    assert lo > 0 and abs(hi - (1 - 0.025 ** (1 / 16))) < 0.01


def test_small_test_disagreement():
    out = sub.analyze(2, 20, 7, 20)
    assert out["ci"][0] == 0.0
    assert out["bootstrap_says"] == "unclear" and out["bayes_says"] == "B", out


def test_moderate_test_is_unclear_for_both():
    out = sub.analyze(30, 200, 40, 200)
    assert out["bootstrap_says"] == "unclear" and out["bayes_says"] == "unclear"
    assert 0.85 < out["prob_b_better"] < 0.95


def test_report():
    words = sub.REPORT.split()
    assert len(words) >= 100, f"{len(words)} words"
    text = sub.REPORT.lower()
    assert "prior" in text and "small" in text and "zero" in text
