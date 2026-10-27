import numpy as np
import sub

Xtr, ytr = sub.make_digits(2000, 0)
Xte, yte = sub.make_digits(1000, 1)
params = sub.train(Xtr, ytr, seed=0)


def _linear_baseline():
    W = np.zeros((64, 10))
    b = np.zeros(10)
    Y = np.eye(10)[ytr]
    for _ in range(500):
        Z = Xtr @ W + b
        Z -= Z.max(axis=1, keepdims=True)
        P = np.exp(Z)
        P /= P.sum(axis=1, keepdims=True)
        G = (P - Y) / 2000
        W -= 0.5 * (Xtr.T @ G + 1e-3 * W)
        b -= 0.5 * G.sum(axis=0)
    return float(np.mean((Xte @ W + b).argmax(axis=1) == yte))


def test_two_hidden_layers():
    assert len([k for k in params if k.startswith("W")]) == 3


def test_grad_check_of_the_backward_pass():
    p = sub.init([64, 6, 5, 10], seed=3)
    X, y = Xtr[:6], ytr[:6]
    _, g = sub.loss_and_grads(p, X, y)
    for k in ["W1", "b2", "W3"]:
        num = np.zeros_like(p[k])
        for idx in np.ndindex(p[k].shape):
            old = p[k][idx]
            p[k][idx] = old + 1e-6
            lp, _ = sub.loss_and_grads(p, X, y)
            p[k][idx] = old - 1e-6
            lm, _ = sub.loss_and_grads(p, X, y)
            p[k][idx] = old
            num[idx] = (lp - lm) / 2e-6
        rel = np.linalg.norm(g[k] - num) / (np.linalg.norm(g[k]) + np.linalg.norm(num) + 1e-12)
        assert rel < 1e-5, (k, rel)


def test_accuracy_target():
    acc = sub.evaluate(params, Xte, yte)
    assert acc >= 0.88, acc


def test_beats_linear_baseline():
    assert sub.evaluate(params, Xte, yte) >= _linear_baseline() + 0.10


def test_report():
    assert len(sub.REPORT.split()) >= 60
    assert "linear" in sub.REPORT.lower()
