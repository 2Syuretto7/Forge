import numpy as np
import sub

Xte, yte = sub.make_digits(1000, 1)
PARAMS, LOSSES = sub.train(seed=0)


def _hidden_weights(p, width):
    return [k for k, v in p.items() if np.ndim(v) == 2 and v.shape == (width, width)]


def test_at_least_30_hidden_layers():
    assert sub.DEPTH >= 30
    assert len(_hidden_weights(sub.init_model(sub.DEPTH, 16, seed=0), 16)) >= 30


def test_grad_check():
    X, y = sub.make_digits(6, 3)
    p = sub.init_model(3, 7, seed=1)
    for k in p:
        p[k] = p[k] + 0.05 * np.random.default_rng(len(k)).normal(size=p[k].shape)
    _, g = sub.loss_and_grads(p, X, y)
    assert sorted(g) == sorted(p)
    for k in p:
        for idx in list(np.ndindex(p[k].shape))[:6]:
            old = p[k][idx]
            p[k][idx] = old + 1e-6
            lp, _ = sub.loss_and_grads(p, X, y)
            p[k][idx] = old - 1e-6
            lm, _ = sub.loss_and_grads(p, X, y)
            p[k][idx] = old
            assert abs((lp - lm) / 2e-6 - g[k][idx]) < 1e-6, (k, idx)


def test_gradients_balanced_at_init():
    X, y = sub.make_digits(200, 0)
    p = sub.init_model(sub.DEPTH, 48, seed=0)
    _, g = sub.loss_and_grads(p, X, y)
    rms = [float(np.sqrt(np.mean(g[k] ** 2))) for k in _hidden_weights(p, 48)]
    assert len(rms) >= 30 and max(rms) / min(rms) < 30, (min(rms), max(rms))


def test_training_is_stable():
    L = np.array(LOSSES)
    assert np.all(np.isfinite(L)) and len(L) >= 100
    assert L[-50:].mean() < 0.3 * L[:50].mean()


def test_accuracy():
    acc = sub.evaluate(PARAMS, Xte, yte)
    assert acc >= 0.85, acc


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    for word in ("residual", "norm", "initiali"):
        assert word in text, word
    assert "learning rate" in text or "warmup" in text
