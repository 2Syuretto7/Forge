import numpy as np
import sub


def test_layout():
    x, y, m = sub.build_example([5, 6], [7, 8, 9], 1, 2, 3, 0, 10)
    assert x.tolist() == [1, 5, 6, 2, 7, 8, 9, 3, 0, 0]
    assert y.tolist() == [5, 6, 2, 7, 8, 9, 3, 0, 0, 0]
    assert m.tolist() == [0, 0, 0, 1, 1, 1, 1, 0, 0, 0]


def test_truncation():
    x, y, m = sub.build_example([5, 6, 7, 8], [9, 9, 9], 1, 2, 3, 0, 6)
    assert len(x) == len(y) == len(m) == 6
    assert y.tolist() == [5, 6, 7, 8, 2, 9] and m.tolist() == [0, 0, 0, 0, 0, 1]
