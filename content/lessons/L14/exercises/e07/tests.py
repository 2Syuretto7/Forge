import numpy as np
import sub

rng = np.random.default_rng(7)
E = rng.normal(size=(6, 4)) * 0.5
b = rng.normal(size=6) * 0.1
x = np.array([0, 3, 3, 5, 1])
y = np.array([2, 2, 0, 4, 3])


def test_grad_tied_embeddings():
    _, dE, db = sub.tied_bigram_loss(E, b, x, y)
    num = np.zeros_like(E)
    for idx in np.ndindex(E.shape):
        P = E.copy()
        P[idx] += 1e-6
        lp = sub.tied_bigram_loss(P, b, x, y)[0]
        P[idx] -= 2e-6
        num[idx] = (lp - sub.tied_bigram_loss(P, b, x, y)[0]) / 2e-6
    assert np.allclose(dE, num, atol=1e-8)
    nb = np.array([(sub.tied_bigram_loss(E, b + e, x, y)[0] - sub.tied_bigram_loss(E, b - e, x, y)[0]) / 2e-6 for e in np.eye(6) * 1e-6])
    assert np.allclose(db, nb, atol=1e-8)


def test_loss_value():
    loss, _, _ = sub.tied_bigram_loss(np.zeros((5, 3)), np.zeros(5), np.array([0, 1]), np.array([2, 3]))
    assert np.isclose(loss, np.log(5))
