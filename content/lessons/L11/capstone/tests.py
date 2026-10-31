import unittest
import numpy as np
import sub


def test_parameter_count():
    for n_layer, d in [(2, 32), (3, 64)]:
        m = sub.GPT(len(sub.chars), sub.CTX, d, n_layer, d // 16)
        assert sub.non_embedding_params(m) == n_layer * (12 * d * d + 13 * d) + 2 * d


def test_sweep():
    assert len(sub.runs) == len(sub.CFG["widths"]) * len(sub.CFG["batches"])
    for r in sub.runs:
        assert r["C"] == 6 * r["N"] * r["D"]
    by_size = {}
    for r in sub.runs:
        by_size.setdefault(r["d"], []).append(r["loss"])
    for losses in by_size.values():
        assert losses[-1] < losses[0], losses


def test_frontier():
    n1, d1, l1 = sub.optimal_allocation(1e12, sub.fit)
    n2, d2, l2 = sub.optimal_allocation(1e13, sub.fit)
    assert abs(6 * n1 * d1 / 1e12 - 1) < 1e-9 and n2 > n1 and d2 > d1 and l2 < l1
    for C in [1e10, 1e12, 1e14]:
        n, d, l = sub.constrained_allocation(C, sub.fit, 1e6)
        assert d <= 1e6 * (1 + 1e-12) and abs(6 * n * d / C - 1) < 1e-9
        assert l >= sub.optimal_allocation(C, sub.fit)[2] - 1e-12


def test_fit_describes_the_sweep():
    if sub.SMALL:
        raise unittest.SkipTest("the fit is checked on the full sweep")
    assert sub.fit_rmse < 0.03, sub.fit_rmse
    assert 0 <= sub.fit["E"] < min(sub.L), sub.fit


def test_prediction_made_first_and_accurate():
    assert sub.predicted_at < sub.heldout_started
    if sub.SMALL:
        raise unittest.SkipTest("the prediction is checked on the full sweep")
    assert abs(sub.prediction_error) < 0.08, sub.prediction_error


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "predict" in text and "alpha" in text and "beta" in text
