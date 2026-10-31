import numpy as np
import sub


def test_detect():
    losses = list(2.0 - 0.001 * np.arange(200) + 0.01 * np.sin(np.arange(200)))
    assert sub.detect_spikes(losses, 50, 5) == []
    losses[120] = 3.0
    losses[150] = float("nan")
    assert sub.detect_spikes(losses, 50, 5) == [121, 151]
    assert sub.detect_spikes([5.0] * 10, 20, 5) == []


def test_rollback_point():
    assert sub.rollback_point(700, 100) == 600
    assert sub.rollback_point(702, 100) == 700
    assert sub.rollback_point(101, 100) == 0
