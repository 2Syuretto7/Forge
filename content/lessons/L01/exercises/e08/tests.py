import numpy as np
import sub

P = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.3, 0.3, 0.4], [0.6, 0.3, 0.1]])
y = np.array([0, 1, 1, 2])


def test_accuracy_and_log_loss():
    assert sub.accuracy(P, y) == 0.5
    expected = -np.mean(np.log([0.7, 0.8, 0.3, 0.1]))
    assert abs(sub.log_loss(P, y) - expected) < 1e-12


def test_log_loss_clips_zeros():
    Q = np.array([[1.0, 0.0], [0.5, 0.5]])
    v = sub.log_loss(Q, np.array([1, 0]))
    assert np.isfinite(v) and v > 10


def test_confusion_matrix():
    C = sub.confusion_matrix(P, y, 3)
    assert C.tolist() == [[1, 0, 0], [0, 1, 1], [1, 0, 0]]
    assert np.trace(C) == 2 and C.sum() == 4
