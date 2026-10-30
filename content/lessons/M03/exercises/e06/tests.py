import sub


def test_hunt():
    assert sub.hunt(lambda n: n * n >= n, range(-5, 5)) is None
    assert sub.hunt(lambda n: n < 7, range(100)) == 7
    assert sub.hunt(lambda x: x * x >= x, [0, 1, 2, 0.5, 3]) == 0.5


def test_hunt_count():
    assert sub.hunt_count(lambda n: n % 2 == 0 or n == 1 or n == 3, range(10)) == (5, 6)
    assert sub.hunt_count(lambda n: True, range(10)) == (None, 10)


def test_hunt_pairs():
    assert sub.hunt_pairs(lambda a, b: abs(a + b) <= abs(a) + abs(b), range(-5, 6)) is None
    assert sub.hunt_pairs(lambda a, b: (a + b) ** 2 == a * a + b * b, range(-2, 3)) == (-2, -2)
