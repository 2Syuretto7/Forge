import random
import sub


def test_examples():
    assert sub.squaring_keeps_order(2, 3)
    assert not sub.squaring_keeps_order(-3, 2)
    assert not sub.squaring_keeps_order(-3, -2)


def test_counterexample():
    pair = sub.find_counterexample()
    assert pair is not None
    a, b = pair
    assert a < b and a * a >= b * b and a < 0


def test_safe_pairs_never_fail():
    rnd = random.Random(9)
    for _ in range(5000):
        a, b = sorted((rnd.uniform(-10, 10), rnd.uniform(-10, 10)))
        if a < b and sub.safe_to_square(a, b):
            assert sub.squaring_keeps_order(a, b)
