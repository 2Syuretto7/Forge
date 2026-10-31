import numpy as np
import sub

RES = sub.lab()


def test_ten_quadratics():
    assert len(RES) == 10
    assert {(r["kappa"], r["step"]) for r in RES} == {(k, s) for k in (10, 30, 100, 300, 1000) for s in ("inverse_L", "best")}


def test_predictions_within_15_percent():
    for r in RES:
        assert abs(r["actual"] - r["predicted"]) <= 0.15 * r["predicted"], r
        assert r["actual"] <= r["bound"], r


def test_tenfold():
    best = {r["kappa"]: r["actual"] for r in RES if r["step"] == "best"}
    assert 8 < best[1000] / best[100] < 12, best


def test_prediction_without_running():
    A = sub.quadratic(np.array([1.0, 4.0]), 3)
    assert sub.predicted_iterations(A, np.array([1.0, 0.0]), 0.25) == sub.gd_iterations(A, np.array([1.0, 0.0]), 0.25)
