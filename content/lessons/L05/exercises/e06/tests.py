import math
import sub


def test_warmup_cosine_shape():
    T, W, peak, floor = 1100, 100, 0.003, 1e-4
    vals = [sub.warmup_cosine(t, T, W, peak, floor) for t in range(0, T + 1)]
    assert vals[0] == 0 and abs(vals[W] - peak) < 1e-15 and abs(vals[T] - floor) < 1e-15
    assert all(a <= b for a, b in zip(vals[:W], vals[1:W + 1]))
    assert all(a >= b for a, b in zip(vals[W:T], vals[W + 1:T + 1]))
    assert abs(sub.warmup_cosine(T + 50, T, W, peak, floor) - floor) < 1e-15


def test_value_from_derivation():
    assert abs(sub.warmup_cosine(600, 1100, 100, 0.003) - 0.0015) < 1e-15
    assert abs(sub.warmup_cosine(50, 1100, 100, 0.003) - 0.0015) < 1e-15


def test_warmup_linear():
    assert abs(sub.warmup_linear(1100, 1100, 100, 0.01)) < 1e-15
    assert abs(sub.warmup_linear(600, 1100, 100, 0.01) - 0.005) < 1e-15
    assert abs(sub.warmup_linear(100, 1100, 100, 0.01) - 0.01) < 1e-15


def test_inverse_sqrt():
    assert abs(sub.inverse_sqrt(400, 100, 0.01) - 0.005) < 1e-15
    assert abs(sub.inverse_sqrt(100, 100, 0.01) - 0.01) < 1e-15
    assert abs(sub.inverse_sqrt(25, 100, 0.01) - 0.0025) < 1e-15
    assert sub.inverse_sqrt(10000, 100, 0.01) == 0.01 * math.sqrt(0.01)
