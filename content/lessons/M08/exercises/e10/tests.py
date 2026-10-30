import math
import sub


def test_log10_comb():
    for n, k in [(52, 5), (200, 100), (1000, 3)]:
        assert abs(sub.log10_comb(n, k) - math.log10(math.comb(n, k))) < 1e-9
        assert sub.digits_of_comb(n, k) == len(str(math.comb(n, k)))


def test_huge():
    d = sub.digits_of_comb(10 ** 6, 256)
    assert d == len(str(math.comb(10 ** 6, 256)))
    assert d > 1000


def test_batches():
    assert sub.steps_per_epoch(1281167, 256) == 5005
    assert sub.epochs_before_repeat_is_likely(10 ** 6, 256) > 500
