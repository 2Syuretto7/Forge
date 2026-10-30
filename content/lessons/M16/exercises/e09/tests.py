import sub


def test_synthetic():
    lin = [0.5 ** k for k in range(60)]
    quad = [0.09 ** (2 ** k) for k in range(6)]
    gold = (1 + 5 ** 0.5) / 2
    sup = [0.09 ** (gold ** k) for k in range(8)]
    assert sub.classify(lin) == "linear" and all(abs(r - 0.5) < 1e-12 for r in sub.rates(lin))
    assert sub.classify(quad) == "quadratic"
    assert sub.classify(sup) == "superlinear"
    assert sub.orders([0.5]) == []


def test_errors():
    assert sub.errors([1.0, 1.5, 1.4], 1.4) == [abs(1.0 - 1.4), abs(1.5 - 1.4), 0.0]
