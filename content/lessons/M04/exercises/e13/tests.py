import sub

DATA = [1.0, 2.0, 2.5, 3.0, 50.0]


def test_pipeline_order():
    assert sub.pipeline([lambda x: x + 1, lambda x: 2 * x])(3) == 8
    assert sub.pipeline([])(3) == 3


def test_standardize():
    z = sub.standardize(DATA)
    assert abs(sum(z)) < 1e-12
    assert abs(sum(v * v for v in z) / len(z) - 1) < 1e-12


def test_order_matters():
    assert sub.order_matters(DATA, -3, 3)
    assert not sub.order_matters([1.0, 2.0, 3.0], -10, 10), "clipping that changes nothing commutes"
    clipped_first = sub.pipeline([lambda v: sub.clip(v, -3, 3), sub.standardize])(DATA)
    assert max(clipped_first) < 2.0, "after clipping the raw data, the outlier is ordinary"
