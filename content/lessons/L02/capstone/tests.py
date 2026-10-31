import numpy as np
import sub

PS = list(range(1, 81))
risks, smins = sub.curve(PS, 0.0, range(10), 0.3)


def _ref_point(p, lam, seeds=range(10)):
    tot = 0.0
    for s in seeds:
        X, y, beta, lam_x, W = sub.make_problem(s, 0.3)
        Phi = X @ W[:p].T
        n = Phi.shape[0]
        if lam == 0:
            w = Phi.T @ np.linalg.solve(Phi @ Phi.T, y) if p > n else np.linalg.lstsq(Phi, y, rcond=None)[0]
        else:
            w = np.linalg.solve(Phi.T @ Phi + lam * np.eye(p), Phi.T @ y) if p <= n else Phi.T @ np.linalg.solve(Phi @ Phi.T + lam * np.eye(n), y)
        d = beta - W[:p].T @ w
        tot += np.sum(lam_x * d * d)
    return tot / len(list(seeds))


def test_curve_matches_reference():
    for p in [3, 12, 35, 70]:
        assert abs(risks[p - 1] - _ref_point(p, 0.0)) < 1e-8 * max(1, risks[p - 1])


def test_peak_at_the_threshold():
    assert sub.peak(PS, risks) == 20
    assert int(np.argmin(smins[10:30])) + 11 == 20, "the smallest singular value bottoms out at p = n"


def test_second_descent_beats_the_first():
    assert min(risks[40:]) < min(risks[:15])


def test_ridge_removes_the_peak():
    r1, _ = sub.curve(PS, 1.0, range(10), 0.3)
    assert r1[19] < risks[19] / 10
    assert r1[19] < 3 * min(r1)


def test_report():
    t = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 100
    assert "singular" in t and "ridge" in t and "threshold" in t
