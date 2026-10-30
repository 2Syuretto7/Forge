import numpy as np
import sub


def test_thresholds():
    assert abs(sub.overflow_threshold(np.float32) - 88.72) < 0.01
    assert abs(sub.overflow_threshold(np.float64) - 709.78) < 0.01
    assert abs(sub.overflow_threshold(np.float16) - 11.09) < 0.01


def test_first_overflow():
    assert sub.first_overflow(np.float32) == 89
    assert sub.first_overflow(np.float16) == 12


def test_safe_range():
    lo, hi = sub.safe_range(np.float16)
    assert hi == 11 and -18 <= lo <= -15
