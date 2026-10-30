import math
import sub

XS = [i / 19 for i in range(20)]
YS = [2.0 * x + 0.5 for x in XS]


def test_square():
    assert sub.square_grad(3.0) == 6.0


def test_zeroing_matters():
    w, b = sub.fit_line(XS, YS, 2000, 0.5, True)
    assert abs(w - 2) < 1e-6 and abs(b - 0.5) < 1e-6
    w2, b2 = sub.fit_line(XS, YS, 200, 0.5, False)
    assert not (abs(w2 - 2) < 0.1 and abs(b2 - 0.5) < 0.1)
    assert not math.isfinite(w2) or abs(w2) > 10 or abs(w2 - 2) > 0.1
