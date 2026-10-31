import numpy as np
import sub

TRUE = 14.392726722865723


def test_order():
    f, b = sub.forward(10**6), sub.backward(10**6)
    assert abs(b - TRUE) < 1e-4, b
    assert abs(f - TRUE) > 1e-2, f
    assert sub.harmonic_terms(3).dtype == np.float32


def test_not_associative():
    a, b, c = np.float32(1e8), np.float32(-1e8), np.float32(1.0)
    assert sub.sequential_sum32([a, b, c]) == 1.0
    assert sub.sequential_sum32([a, c, b]) == 0.0
