import numpy as np
import sub


def test_mask():
    m = sub.packed_attention_mask([2, 3])
    expected = np.array([
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1],
    ], dtype=bool)
    assert m.dtype == bool and np.array_equal(m, expected)


def test_positions():
    assert sub.packed_positions([2, 3, 1]).tolist() == [0, 1, 0, 1, 2, 0]
