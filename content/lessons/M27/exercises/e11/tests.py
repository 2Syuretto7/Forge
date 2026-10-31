import numpy as np
import sub


def test_naive_overflows_in_float64():
    z = np.array([1000.0, 0.0, -5.0])
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        bad = sub.naive_logprob(z, 0)
    assert not np.isfinite(bad), "the naive version should break on huge logits"
    assert abs(sub.stable_logprob(z, 0)) < 1e-12


def test_naive_underflows_in_float32():
    z = np.array([0.0, -120.0], dtype=np.float32)
    with np.errstate(divide="ignore", under="ignore"):
        bad = sub.naive_logprob(z, 1)
    assert np.isneginf(bad), "e^-120 is below the smallest float32"
    good = sub.stable_logprob(z, 1)
    assert good.dtype == np.float32
    assert abs(float(good) + 120.0) < 1e-3


def test_agree_on_moderate_inputs():
    z = np.array([0.3, -1.2, 2.0, 0.0])
    for y in range(4):
        assert abs(sub.naive_logprob(z, y) - sub.stable_logprob(z, y)) < 1e-12
