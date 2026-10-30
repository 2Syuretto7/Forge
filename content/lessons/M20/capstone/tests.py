import numpy as np
import sub

REP = sub.report()


def test_grad_change_of_variables():
    assert set(REP) == {"exponential", "cauchy", "box-muller", "disc", "correlated"}
    for name, (cov, _) in REP.items():
        assert cov < 1e-6, (name, cov)


def test_histograms():
    for name, (_, hist) in REP.items():
        assert hist < 0.1, (name, hist)


def test_grad_wrong_density_fails():
    wrong = lambda y: np.exp(-2 * np.asarray(y, dtype=float))  # noqa: E731
    assert sub.cov_check(sub.exp_inverse, wrong, [0.5, 1.0]) > 0.4
    rng = np.random.default_rng(5)
    assert sub.hist_check_1d(sub.exp_map(1 - rng.random(200_000)), wrong, 0, 4, 40) > 0.3


def test_maps_invert():
    u = np.array([0.37, 0.81])
    for m, inv in [(sub.bm_map, sub.bm_inverse), (sub.disc_map, sub.disc_inverse), (sub.corr_map, sub.corr_inverse)]:
        assert np.allclose(inv(m(u)), u)
    assert abs(sub.cauchy_inverse(sub.cauchy_map(0.3)) - 0.3) < 1e-12
