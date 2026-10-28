import warnings
import numpy as np
import sub

rng = np.random.default_rng(1)
X = np.concatenate([
    rng.normal(size=3000) * np.exp(rng.uniform(-25, 12, size=3000)),
    [0.0, 0.1, 1 / 3, 1 + 2 ** -11, 1 + 3 * 2 ** -11, 65504, 65519, 65520, 1e5, 2 ** -24, 2 ** -25, 3e-8, -2.5, 2 ** -14],
])


def test_matches_numpy_float16():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ref = X.astype(np.float16).astype(np.float64)
    assert np.array_equal(sub.round_to_format(X, 5, 10), ref)


def test_bfloat16_examples():
    r = sub.round_to_format(np.array([1.0 + 2 ** -8, 1.0 + 3 * 2 ** -8, 3e38, 4e38, 1e-40]), 8, 7)
    assert r[0] == 1.0 and r[1] == 1.0 + 2 ** -6
    assert np.isfinite(r[2]) and np.isinf(r[3]) and 0 < r[4] < 1e-39
