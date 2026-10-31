import sub


def test_memorizes_noise():
    train, test = sub.random_feature_probe(100, 1000, 200)
    assert train == 1.0 and 0.4 < test < 0.6
    train2, _ = sub.random_feature_probe(1000, 1000, 20)
    assert train2 < 0.7
