import warnings
import numpy as np
import sub


def test_threshold():
    assert abs(sub.overflow_threshold() - np.log(65504)) < 1e-9
    assert sub.overflow_threshold(np.float32) > 88


def test_naive_breaks_and_stable_does_not():
    x = np.array([[1.0, 12.0, 3.0], [0.5, -1.0, 2.0]], dtype=np.float16)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        naive = sub.naive_softmax(x)
    assert not np.all(np.isfinite(naive[0]))
    s = sub.stable_softmax(x)
    assert s.dtype == np.float16 and np.all(np.isfinite(s))
    ref = np.exp(x.astype(np.float64) - x.max(axis=1, keepdims=True))
    assert np.allclose(s, ref / ref.sum(axis=1, keepdims=True), atol=1e-3)
