import numpy as np
import sub


def test_one_over_root_d():
    for d in [10, 100, 300]:
        assert abs(sub.typical_cosine(d) * np.sqrt(d) - 1) < 0.08, d


def test_high_dimension():
    assert sub.fraction_nearly_perpendicular(1000, 0.087) > 0.99
    assert sub.fraction_nearly_perpendicular(2, 0.087) < 0.1
