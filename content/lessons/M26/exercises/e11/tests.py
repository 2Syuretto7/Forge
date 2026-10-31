import numpy as np
import sub


def test_error_bound():
    x = (np.random.default_rng(11).random(10**6) * 200 - 100).astype(np.float32)
    for bits in (10, 7, 3):
        r = sub.round_mantissa(x, bits)
        assert r.dtype == np.float32
        err = np.max(np.abs(r.astype(np.float64) - x) / np.abs(x.astype(np.float64)))
        assert err <= sub.max_relative_error(bits) * (1 + 1e-6), (bits, err)


def test_ties_to_even():
    one = np.float32(1.0)
    assert sub.round_mantissa(np.array([one + np.float32(2.0**-8)]), 7)[0] == one
    assert sub.round_mantissa(np.array([one + np.float32(3 * 2.0**-8)]), 7)[0] == one + np.float32(2.0**-6)
    assert sub.round_mantissa(np.array([np.float32(0.1)]), 23)[0] == np.float32(0.1)


def test_accumulator_stalls_in_bf16():
    bf16 = sub.accumulate(1e-3, 3000, 7)
    fp32 = sub.accumulate(1e-3, 3000, 23)
    assert abs(fp32 - 3.0) < 1e-3
    assert bf16 < 1.0, bf16
