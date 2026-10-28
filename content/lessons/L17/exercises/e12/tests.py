import numpy as np
import sub


def test_range():
    big, tiny = np.array([1e5]), np.array([1e-9])
    assert not sub.survives(big, sub.fp16)[0] and sub.survives(big, sub.bf16)[0]
    assert not sub.survives(tiny, sub.fp16)[0] and sub.survives(tiny, sub.bf16)[0]


def test_precision():
    a, b = np.array([1.000]), np.array([1.001])
    assert sub.resolves(a, b, sub.fp16)[0] and not sub.resolves(a, b, sub.bf16)[0]
