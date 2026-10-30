import numpy as np
import sub

rng = np.random.default_rng(1)


def test_same_result():
    A, B = rng.normal(size=(6, 4, 5)), rng.normal(size=(6, 5, 3))
    C = sub.batched(A, B)
    assert C.shape == (6, 4, 3)
    assert np.allclose(sub.batched_loop(A, B), C)


def test_measure():
    flops, dt, rate = sub.measure(4, 64)
    assert flops == 2 * 4 * 64 ** 3
    assert dt > 0 and abs(rate - flops / dt) < 1e-6 * rate
