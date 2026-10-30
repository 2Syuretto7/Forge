import random
import sub


def test_basic():
    p = sub.softmax([1.0, 2.0, 3.0])
    assert abs(sum(p) - 1) < 1e-15 and all(x > 0 for x in p)
    assert p[0] < p[1] < p[2]
    assert all(abs(a - b) < 1e-15 for a, b in zip(p, sub.softmax_naive([1.0, 2.0, 3.0])))


def test_shift_invariance():
    rnd = random.Random(0)
    for _ in range(200):
        z = [rnd.uniform(-5, 5) for _ in range(6)]
        c = rnd.uniform(-50, 50)
        assert all(abs(a - b) < 1e-12 for a, b in zip(sub.softmax(z), sub.softmax([v + c for v in z])))
        assert sub.argmax(sub.softmax(z)) == sub.argmax(z)


def test_large_scores():
    p = sub.softmax([1000.0, 999.0, 998.0])
    assert abs(p[0] - 0.6652409557748219) < 1e-12
    try:
        sub.softmax_naive([1000.0, 999.0, 998.0])
    except OverflowError:
        return
    raise AssertionError("math.exp(1000) should overflow in the naive version")
