import numpy as np
import sub


def test_prediction_matches_runs():
    for kappa in (10, 100, 1000):
        assert sub.run_iterations(kappa) == sub.predict_iterations(kappa), kappa


def test_slope_near_one():
    kappas = [10.0, 100.0, 1e3, 1e4, 1e5]
    counts = [sub.predict_iterations(k) for k in kappas]
    assert all(a < b for a, b in zip(counts, counts[1:]))
    s = sub.slope(kappas, counts)
    assert 0.85 < s < 1.05, (s, counts)


def test_spectrum():
    lam = sub.spectrum(100.0, 5)
    assert np.allclose(lam, [1, np.sqrt(10), 10, np.sqrt(1000), 100])
