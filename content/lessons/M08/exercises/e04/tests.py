import random
import sub


def test_rows():
    assert sub.pascal_rows(4) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    assert sub.poly_power(5)[2] == 10


def test_invariant_sums():
    for n, row in enumerate(sub.pascal_rows(30)):
        assert sum(row) == 2 ** n
        if n >= 1:
            assert sum((-1) ** k * c for k, c in enumerate(row)) == 0
    rnd = random.Random(0)
    for _ in range(200):
        a, b, n = rnd.randint(-9, 9), rnd.randint(-9, 9), rnd.randint(0, 25)
        assert sum(sub.expand(a, b, n)) == (a + b) ** n
