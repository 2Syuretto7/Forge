import numpy as np
import sub


A, S = sub.make_matrix()


def test_error_target():
    U, sv, Vt = sub.rsvd(A, 10)
    assert U.shape == (2000, 10) and Vt.shape == (10, 400)
    assert sub.meets_target(A, U, sv, Vt, S, 10)
    assert not sub.meets_target(A, U[:, :5], sv[:5], Vt[:5], S, 10)


def test_speedup():
    r = sub.speedup(A, 10)
    assert r["ratio"] > 5, r


def test_kernels():
    ks = sub.kernels(2000, 400, 10, 10, 1)
    assert len(ks) == 4
    assert all(k["flops"] == 2 * 2000 * 400 * 20 for k in ks)
    assert ks[0]["bytes"] == (2000 * 400 + 400 * 20 + 2000 * 20) * 8
    pl = sub.placements(ks, sub.PEAK, sub.BW)
    assert all(abs(p["intensity"] - p["flops"] / p["bytes"]) < 1e-12 for p in pl)
    assert all(p["bound"] == "compute" for p in pl)
    assert sub.placements(sub.kernels(2000, 400, 1, 0, 0), sub.PEAK, sub.BW)[0]["bound"] == "memory"


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for w in ("intensity", "compute-bound", "power iteration", "faster"):
        assert w in text, w
