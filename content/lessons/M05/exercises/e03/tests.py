import random
import sub


def test_sigma():
    assert sub.sigma(lambda k: k, 1, 100) == 5050
    assert sub.sigma(lambda k: k * k, 1, 3) == 14
    assert sub.sigma(lambda k: 1, 5, 4) == 0


def test_shift_and_split():
    f = lambda k: 3 * k * k - k
    assert sub.shift_index(f, 2, 20, 7) == sub.sigma(f, 2, 20)
    a, b = sub.split(f, 1, 10, 30)
    assert a + b == sub.sigma(f, 1, 30)


def test_invariant_linearity():
    rnd = random.Random(1)
    for _ in range(300):
        a, b = rnd.randint(-5, 5), rnd.randint(-5, 5)
        p, q = rnd.randint(0, 3), rnd.randint(0, 3)
        f = lambda k, p=p: k ** p
        g = lambda k, q=q: (-1) ** k * k ** q
        lo, hi = rnd.randint(-10, 5), rnd.randint(-5, 30)
        assert sub.sigma(lambda k: a * f(k) + b * g(k), lo, hi) == a * sub.sigma(f, lo, hi) + b * sub.sigma(g, lo, hi)
