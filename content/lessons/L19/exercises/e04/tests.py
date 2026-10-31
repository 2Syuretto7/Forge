import numpy as np
import sub

rng = np.random.default_rng(2)
d = 16
direction = rng.normal(size=d)
A = rng.normal(size=(600, d))
y = (A @ direction + 0.3 * rng.normal(size=600) > 0).astype(float)


def test_grad_probe():
    w, b = rng.normal(size=d) * 0.1, 0.2
    _, dw, db = sub.probe_loss(w, b, A, y)
    num = [(sub.probe_loss(w + e, b, A, y)[0] - sub.probe_loss(w - e, b, A, y)[0]) / 2e-6 for e in np.eye(d) * 1e-6]
    assert np.allclose(dw, num, atol=1e-8)
    assert abs(db - (sub.probe_loss(w, b + 1e-6, A, y)[0] - sub.probe_loss(w, b - 1e-6, A, y)[0]) / 2e-6) < 1e-8


def test_held_out_accuracy():
    w, b = sub.train_probe(A[:400], y[:400])
    assert sub.probe_accuracy(w, b, A[400:], y[400:]) > 0.9
