import numpy as np
import sub

X, y = sub.make_dataset()
out = sub.train_and_evaluate(X[:600], y[:600], X[600:], y[600:])


def test_targets():
    assert out["accuracy"] >= 0.87, out["accuracy"]
    assert out["log_loss"] <= 0.30, out["log_loss"]
    assert out["ece"] <= 0.06, out["ece"]


def test_metrics_are_consistent():
    C = np.asarray(out["confusion"])
    assert C.shape == (3, 3) and C.sum() == 300
    assert abs(np.trace(C) / 300 - out["accuracy"]) < 1e-12


def test_test_rows_do_not_influence_training():
    X2 = X.copy()
    X2[600:] = X2[600:] * 3 + 100  # corrupt the test features only
    out2 = sub.train_and_evaluate(X2[:600], y[:600], X2[600:], y[600:])
    assert np.allclose(out2["W"], out["W"]) and np.allclose(out2["b"], out["b"]), "training must use training rows only"


def test_report():
    words = sub.REPORT.split()
    assert len(words) >= 80, f"{len(words)} words"
    t = sub.REPORT.lower()
    assert "standard" in t and "calibrat" in t
