import numpy as np
import sub


def gs(w, rng):
    return w + rng.standard_normal(w.shape)


def test_schedules():
    assert sub.inverse_time(0, 0.5, 10) == 0.5 and abs(sub.inverse_time(10, 0.5, 10) - 0.25) < 1e-15
    assert sub.step_decay(250, 1.0, 100) == 0.25
    assert sub.cosine(0, 1.0, 100) == 1.0 and abs(sub.cosine(100, 1.0, 100)) < 1e-15 and abs(sub.cosine(50, 1.0, 100) - 0.5) < 1e-15


def test_decay_beats_constant():
    rng = np.random.default_rng(8)
    const = sub.sgd_scheduled(gs, np.full(400, 3.0), lambda k: 0.1, 3000, rng) ** 2
    decay = sub.sgd_scheduled(gs, np.full(400, 3.0), lambda k: sub.inverse_time(k, 0.5, 10), 3000, rng) ** 2
    assert abs(np.mean(const) - 0.1 / 1.9) < 0.012
    assert np.mean(decay) < np.mean(const) / 5
