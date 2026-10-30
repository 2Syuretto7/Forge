import numpy as np
import sub


def test_linear():
    x = np.array([[1.0, 2.0, 3.0]])
    W = np.array([[1.0, 0, 0], [0, 1.0, 1.0]])
    assert np.allclose(sub.linear(x, W, np.array([0.5, -1.0])), [[1.5, 4.0]])


def test_wrong_runs_matches_numpy():
    for d_in, d_out in [(3, 3), (3, 4), (4, 3)]:
        x, W, b = np.ones((2, d_in)), np.ones((d_out, d_in)), np.ones(d_out)
        try:
            x @ W + b
            ran = True
        except ValueError:
            ran = False
        assert sub.wrong_runs(d_in, d_out) == ran


def test_detect():
    assert sub.detect_transpose_bug(lambda x, W, b: x @ W + b)
    assert not sub.detect_transpose_bug(lambda x, W, b: (W @ x.T).T + b)
