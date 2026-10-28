import numpy as np
import sub

X, y = sub.make_digits(2000, 0)


class _Nan:
    def step(self, params, grads, lr=None):
        for k in params:
            params[k][...] = np.nan


class _Blowup:
    def step(self, params, grads, lr=None):
        params["b3"][0] = 1e4


def test_sgd_sweep():
    lrs = list(10 ** np.arange(-3, 0.51, 0.5))
    losses = sub.sweep(lambda lr: sub.SGD(lr), lrs, X, y)
    assert len(losses) == 8 and losses[0] > 2.0
    assert 0.3 <= sub.best_lr(lrs, losses) <= 1.5
    assert losses[-1] > 2.0
    assert min(losses) < 0.2


def test_adam_sweep():
    lrs = list(10 ** np.arange(-4, -0.49, 0.5))
    losses = sub.sweep(lambda lr: sub.Adam(lr), lrs, X, y)
    assert 3e-3 <= sub.best_lr(lrs, losses) <= 3e-2
    assert losses[0] > 1.5 and losses[-1] > 1.0


def test_failed_runs_are_inf():
    losses = sub.sweep(lambda lr: _Nan() if lr == 1 else _Blowup(), [1, 2], X, y, steps=3)
    assert losses == [float("inf"), float("inf")]


def test_best_lr():
    assert sub.best_lr([0.1, 0.2, 0.3], [1.0, 0.5, float("inf")]) == 0.2
