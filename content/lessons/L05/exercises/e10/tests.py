import numpy as np
import sub

Xtr, ytr = sub.make_digits(2000, 0)
Xte, yte = sub.make_digits(1000, 1)


class _Recorder:
    def __init__(self):
        self.lrs = []

    def step(self, params, grads, lr=None):
        self.lrs.append(lr)


def test_reproducible_and_length():
    _, a = sub.train(sub.SGD(0.1), Xtr, ytr, 90)
    _, b = sub.train(sub.SGD(0.1), Xtr, ytr, 90)
    assert len(a) == 90 and a == b


def test_schedule_drives_lr():
    rec = _Recorder()
    sub.train(rec, Xtr, ytr, 45, schedule=lambda t: 0.001 * t)
    assert np.allclose(rec.lrs, [0.001 * t for t in range(1, 46)])
    rec = _Recorder()
    sub.train(rec, Xtr, ytr, 5)
    assert rec.lrs == [None] * 5


def test_full_batch_first_loss():
    _, losses = sub.train(sub.SGD(0.1), Xtr, ytr, 3, batch=2000, seed=4)
    first, _ = sub.loss_and_grads(sub.init([64, 64, 32, 10], 4), Xtr, ytr)
    assert abs(losses[0] - first) < 1e-12


def test_sgd_reaches_accuracy():
    params, losses = sub.train(sub.SGD(0.3), Xtr, ytr, 600)
    assert np.mean(losses[-40:]) < 0.5 * np.mean(losses[:40])
    assert sub.evaluate(params, Xte, yte) >= 0.88
