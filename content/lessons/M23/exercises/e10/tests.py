import numpy as np
import sub


def test_edges():
    for n in (256, 1024, 4096, 8192):
        e = sub.sample_cov_spectrum(n, 256, 1)
        lo, hi = sub.mp_edges(n, 256)
        assert abs(e[-1] / hi - 1) < 0.1, (n, e[-1], hi)
        assert abs(e[0] - lo) < 0.1 * max(lo, 0.1), (n, e[0], lo)


def test_error_halves_with_four_times_the_data():
    errs = [sub.spectral_error(n, 256, 2) for n in (1024, 4096)]
    assert 1.6 < errs[0] / errs[1] < 2.4, errs
    assert sub.spectral_error(256, 256, 3) > 2.5
