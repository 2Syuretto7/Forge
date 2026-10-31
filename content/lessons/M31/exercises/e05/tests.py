import math
import sub


def test_counts():
    for m in range(1, 8):
        xs = [0.3 * i + 0.1 * (i % 2) for i in range(m)]
        assert len(sub.threshold_labelings(xs)) == m + 1
        assert len(sub.interval_labelings(xs)) == math.comb(m + 1, 2) + 1


def test_vc_and_sauer():
    assert sub.vc_dimension(sub.threshold_labelings) == 1
    assert sub.vc_dimension(sub.interval_labelings) == 2
    for m in range(1, 9):
        assert len(sub.interval_labelings(list(range(m)))) <= sub.sauer_bound(m, 2)
    assert sub.sauer_bound(10, 3) == 1 + 10 + 45 + 120
