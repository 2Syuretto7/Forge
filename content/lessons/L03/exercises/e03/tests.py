import numpy as np
import sub

rng = np.random.default_rng(3)
Z = rng.normal(size=(7, 4)) * 2
y = rng.integers(0, 4, size=7)


def test_loss_value():
    P = np.exp(Z) / np.exp(Z).sum(axis=1, keepdims=True)
    loss, _ = sub.softmax_ce_forward(Z, y)
    assert abs(loss + np.mean(np.log(P[np.arange(7), y]))) < 1e-12


def test_grad_matches_finite_differences():
    _, c = sub.softmax_ce_forward(Z, y)
    dZ = sub.softmax_ce_backward(c)
    num = np.zeros_like(Z)
    for idx in np.ndindex(Z.shape):
        E = np.zeros_like(Z)
        E[idx] = 1e-6
        num[idx] = (sub.softmax_ce_forward(Z + E, y)[0] - sub.softmax_ce_forward(Z - E, y)[0]) / 2e-6
    assert np.linalg.norm(dZ - num) / (np.linalg.norm(dZ) + np.linalg.norm(num)) < 1e-5
    assert np.allclose(dZ.sum(axis=1), 0, atol=1e-15)


def test_stable():
    loss, _ = sub.softmax_ce_forward(np.array([[1000.0, -1000.0]]), np.array([1]))
    assert np.isfinite(loss) and abs(loss - 2000.0) < 1e-9
