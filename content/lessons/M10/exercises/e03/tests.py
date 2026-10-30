import numpy as np
import sub


def test_shapes_match_numpy():
    cases = [((3, 4), (4, 5)), ((3, 4), (4,)), ((8, 3, 4), (8, 4, 2)), ((8, 3, 4), (1, 4, 2)), ((3, 4), (6, 4, 2)), ((6, 3, 4), (4, 7))]
    for s1, s2 in cases:
        expect = (np.ones(s1) @ np.ones(s2)).shape
        assert sub.matmul_shape(s1, s2) == expect, (s1, s2)


def test_errors():
    for s1, s2 in [((3, 4), (5, 2)), ((2, 3, 4), (3, 4, 5))]:
        try:
            sub.matmul_shape(s1, s2)
        except ValueError:
            continue
        raise AssertionError(f"{s1} @ {s2} should raise ValueError")


def test_flops():
    assert sub.matmul_flops((512, 512), (512, 512)) == 2 * 512 ** 3
    assert sub.matmul_flops((64, 512, 512), (64, 512, 512)) == 17179869184
    assert sub.matmul_flops((10, 20), (20,)) == 400
