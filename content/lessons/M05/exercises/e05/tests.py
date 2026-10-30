import sub


def test_last_outside():
    assert sub.last_outside(lambda n: 1 / n, 0, 0.1, 1000) == 10
    assert sub.last_outside(lambda n: (-1) ** n, 0, 0.5, 1000) == 1000, "this sequence never settles"
    assert sub.last_outside(lambda n: 5, 5, 1e-9, 50) == 0


def test_geometric_N():
    assert sub.geometric_N(0.9, 1e-6) == 132
    assert sub.geometric_N(0.5, 0.001) == 10
    for r, eps in [(0.99, 1e-3), (0.1, 1e-9), (0.75, 0.2)]:
        n = sub.geometric_N(r, eps)
        assert r ** n < eps <= r ** (n - 1)


def test_harmonic_N():
    assert sub.harmonic_N(0.001) == 1001
    assert sub.harmonic_N(0.3) == 4
