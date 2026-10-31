import numpy as np
import sub

rng = np.random.default_rng(2)
GOOD = "the of and to in that it with as for his was he be on by not but at this all from have they".split()
BAD = "click buy free deal now cheap win offer best sale login download casino bonus top".split()


def doc(words, n=40):
    return " ".join(rng.choice(words, n))


docs = [doc(GOOD) for _ in range(30)] + [doc(BAD) for _ in range(30)]
X = np.stack([sub.features(d) for d in docs])
y = np.array([1] * 30 + [0] * 30, dtype=float)


def test_grad_logistic_loss():
    w = rng.normal(size=X.shape[1]) * 0.1
    b = 0.3
    _, dw, db = sub.loss_and_grad(w, b, X, y, 1e-2)
    idx = rng.choice(X.shape[1], 8, replace=False)
    for i in idx:
        e = np.zeros_like(w)
        e[i] = 1e-6
        num = (sub.loss_and_grad(w + e, b, X, y, 1e-2)[0] - sub.loss_and_grad(w - e, b, X, y, 1e-2)[0]) / 2e-6
        assert abs(dw[i] - num) < 1e-8
    nb = (sub.loss_and_grad(w, b + 1e-6, X, y, 1e-2)[0] - sub.loss_and_grad(w, b - 1e-6, X, y, 1e-2)[0]) / 2e-6
    assert abs(db - nb) < 1e-8


def test_classifier_separates_held_out_docs():
    w, b = sub.train(X, y)
    test = [doc(GOOD) for _ in range(10)] + [doc(BAD) for _ in range(10)]
    scores = np.array([sub.features(d) @ w + b for d in test])
    assert np.all(scores[:10] > 0) and np.all(scores[10:] < 0)
