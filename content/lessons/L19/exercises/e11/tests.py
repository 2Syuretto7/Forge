import sub


def test_few_items_cannot_tell():
    lo, hi = sub.compare_models(0.7, 0.6, 20)
    assert lo < 0 < hi


def test_many_items_can():
    lo, hi = sub.compare_models(0.7, 0.6, 2000)
    assert 0 < lo < 0.1 < hi < 0.2
