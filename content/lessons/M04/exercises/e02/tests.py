import random
import sub

sq = lambda x: x * x
inc = lambda x: x + 1
dbl = lambda x: 2 * x


def test_compose():
    assert sub.compose(sq, inc)(2) == 9
    assert sub.compose(inc, sq)(2) == 5


def test_compose_all():
    assert sub.compose_all([sq, inc, dbl])(3) == 49
    assert sub.compose_all([])(7) == 7


def test_commute_points():
    assert sub.commute_points(sq, inc, [-2, -1, 0, 1, 2]) == [0]
    assert sub.commute_points(dbl, lambda x: 3 * x, [-1, 0, 5]) == [-1, 0, 5]


def test_invariant_associative():
    rnd = random.Random(0)
    pool = [sq, inc, dbl, abs, lambda x: x - 3, lambda x: max(0, x), lambda x: x / 2]
    for _ in range(500):
        f, g, h = rnd.choice(pool), rnd.choice(pool), rnd.choice(pool)
        x = rnd.uniform(-5, 5)
        assert sub.compose(f, sub.compose(g, h))(x) == sub.compose(sub.compose(f, g), h)(x)
