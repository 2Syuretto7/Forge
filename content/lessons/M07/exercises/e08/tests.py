import math
import sub


def test_euler():
    assert abs(sub.exp_series(1j * math.pi) + 1) < 1e-12
    for t in [-3.0, 0.5, 2.0, 6.0]:
        assert sub.euler_gap(t) < 1e-12


def test_split_into_cosine_and_sine():
    re, im = sub.real_and_imaginary_terms(0.7)
    assert abs(sum(re) - math.cos(0.7)) < 1e-15 and abs(sum(im) - math.sin(0.7)) < 1e-15
    assert re[1] == 0 and im[0] == 0
    assert abs(re[2] + 0.7 ** 2 / 2) < 1e-15
