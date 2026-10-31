import numpy as np
import sub

BLOCKS = np.array([[0.7, 0.3, 0, 0], [0.4, 0.6, 0, 0], [0, 0, 0.2, 0.8], [0, 0, 0.5, 0.5]])
CYCLE = np.array([[0, 1.0, 0], [0, 0, 1.0], [1.0, 0, 0]])


def test_reducible():
    assert sub.communicating_classes(BLOCKS) == [[0, 1], [2, 3]]
    assert sub.n_stationary(BLOCKS) == 2
    a, b = sub.long_run(BLOCKS, 0), sub.long_run(BLOCKS, 3)
    assert np.allclose(a, [4 / 7, 3 / 7, 0, 0]) and np.allclose(b, [0, 0, 5 / 13, 8 / 13])
    leak = BLOCKS.copy()
    leak[1] = [0.4, 0.5, 0.1, 0]
    assert sub.communicating_classes(leak) == [[0, 1], [2, 3]]
    assert np.allclose(sub.long_run(leak, 0), sub.long_run(leak, 3), atol=1e-6)


def test_periodic():
    assert sub.period(CYCLE, 0) == 3 and sub.n_stationary(CYCLE) == 1
    d1, d2 = sub.long_run(CYCLE, 0, 2000), sub.long_run(CYCLE, 0, 2001)
    assert 0.5 * np.abs(d1 - d2).sum() == 1.0
    lazy = 0.5 * np.eye(3) + 0.5 * CYCLE
    assert sub.period(lazy, 0) == 1
    assert np.allclose(sub.long_run(lazy, 0), np.ones(3) / 3)
