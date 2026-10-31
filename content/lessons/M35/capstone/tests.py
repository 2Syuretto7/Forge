import numpy as np
import sub

N, D, L = sub.make_runs()


def test_fit():
    E, A, alpha, B, beta = sub.fit(N, D, L)
    assert abs(alpha - 0.34) < 0.05 and abs(beta - 0.28) < 0.05


def test_held_out_inside():
    s = sub.bootstrap(N, D, L, B=100)
    assert s.shape == (100, 5)
    Nb, Db, Lb = sub.held_out()
    lo, hi = sub.predict_interval(s, Nb, Db)
    assert lo < Lb < hi and hi - lo < 0.1, (lo, Lb, hi)


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for w in ("bootstrap", "held-out", "interval", "extrapolat"):
        assert w in text, w
