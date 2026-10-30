import math
import random
import sub


def test_frequencies():
    f = sub.frequencies(8)
    assert f[0] == 1 and abs(f[1] - 10000 ** -0.25) < 1e-15 and len(f) == 4


def test_length_is_preserved():
    rnd = random.Random(0)
    x = [rnd.gauss(0, 1) for _ in range(16)]
    for m in [0, 1, 7, 1000]:
        assert abs(math.sqrt(sub.dot(sub.rope(x, m), sub.rope(x, m))) - math.sqrt(sub.dot(x, x))) < 1e-12


def test_only_the_distance_matters():
    rnd = random.Random(1)
    for _ in range(200):
        q = [rnd.gauss(0, 1) for _ in range(8)]
        k = [rnd.gauss(0, 1) for _ in range(8)]
        m, n, s = rnd.randint(0, 500), rnd.randint(0, 500), rnd.randint(-300, 300)
        assert abs(sub.score(q, k, m, n) - sub.score(q, k, m + s, n + s)) < 1e-9
