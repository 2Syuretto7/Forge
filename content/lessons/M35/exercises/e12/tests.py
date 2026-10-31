import numpy as np
import sub


def test_bands_are_honest():
    rng = np.random.default_rng(0)
    x = np.logspace(0, 2, 30)
    x0s = np.array([50.0, 1e3, 1e4])
    errs, ses = [], []
    for _ in range(200):
        e, s = sub.extrapolation_trial(x, np.array([1.7, 2.0, 0.5]), 0.01, x0s, rng)
        errs.append(e)
        ses.append(s)
    rms = sub.rms_error(errs)
    cov = sub.coverage(errs, ses)
    assert rms[0] < rms[1] < rms[2], rms
    assert np.all((cov > 0.88) & (cov < 0.99)), cov
