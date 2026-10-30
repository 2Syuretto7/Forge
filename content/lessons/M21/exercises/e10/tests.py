import sub


def test_split():
    X, y = sub.make_corpus(1000, seed=1)
    a, b, c, d = sub.train_test(X, y, 800)
    assert a.shape == (800, 300) and c.shape == (200, 300) and len(b) == 800


def test_accuracy():
    assert sub.evaluate() > 0.95
