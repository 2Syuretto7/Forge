import numpy as np
import sub


def test_scales():
    rng = np.random.default_rng(0)
    W = sub.xavier(300, 500, rng)
    assert W.shape == (300, 500) and abs(W.std() - np.sqrt(2 / 800)) < 0.002
    W = sub.he(300, 500, rng)
    assert abs(W.std() - np.sqrt(2 / 300)) < 0.002


def test_he_relu_preserves_scale():
    r = sub.depth_rms("he", "relu")
    assert len(r) == 30 and 0.5 < r[-1] < 2.0, r[-1]


def test_xavier_relu_vanishes():
    r = sub.depth_rms("xavier", "relu")
    assert r[-1] < 1e-3, r[-1]
    assert 0.6 < (r[20] / r[10]) ** 0.1 < 0.8


def test_unit_init():
    assert sub.depth_rms("unit", "relu")[-1] > 1e10
    assert sub.depth_rms("unit", "tanh")[-1] > 0.9


def test_xavier_tanh_shrinks_slowly():
    r = sub.depth_rms("xavier", "tanh")
    assert 0.05 < r[-1] < r[0] / 2
