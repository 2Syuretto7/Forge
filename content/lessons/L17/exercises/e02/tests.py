import numpy as np
import sub


def test_fp16_and_bf16():
    h = sub.format_properties(5, 10)
    assert h == {"max": 65504.0, "min_normal": 2.0 ** -14, "min_subnormal": 2.0 ** -24, "eps": 2.0 ** -10}
    b = sub.format_properties(8, 7)
    assert b["min_normal"] == 2.0 ** -126 and b["eps"] == 2.0 ** -7 and abs(b["max"] - 3.3895313892515355e38) < 1e30


def test_against_numpy_finfo():
    for dt, (e, m) in ((np.float16, (5, 10)), (np.float32, (8, 23)), (np.float64, (11, 52))):
        p = sub.format_properties(e, m)
        fi = np.finfo(dt)
        assert p["max"] == float(fi.max) and p["eps"] == float(fi.eps) and p["min_normal"] == float(fi.tiny)


def test_digits():
    assert 3.3 < sub.decimal_digits(10) < 3.4 and 2.4 < sub.decimal_digits(7) < 2.5
