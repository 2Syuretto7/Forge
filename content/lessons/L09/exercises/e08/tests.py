import numpy as np
import sub

rng = np.random.default_rng(8)


def _params():
    return {"W1": rng.normal(size=(3, 2)), "b1": rng.normal(size=2)}


def _grads(p):
    return {k: rng.normal(size=v.shape) for k, v in p.items()}


def test_sgd_plain_and_lr_override():
    p = _params()
    g = _grads(p)
    before = {k: v.copy() for k, v in p.items()}
    sub.SGD(0.1).step(p, g)
    assert all(np.allclose(p[k], before[k] - 0.1 * g[k]) for k in p)
    sub.SGD(0.1).step(p, g, lr=0.5)
    assert all(np.allclose(p[k], before[k] - 0.6 * g[k]) for k in p)


def test_sgd_momentum_and_decay():
    p = _params()
    ref = {k: v.copy() for k, v in p.items()}
    opt = sub.SGD(0.1, momentum=0.9, weight_decay=0.01)
    vel = {k: 0.0 for k in p}
    for _ in range(3):
        g = _grads(p)
        for k in ref:
            gk = g[k] + (0.01 * ref[k] if k.startswith("W") else 0.0)
            vel[k] = 0.9 * vel[k] + gk
            ref[k] = ref[k] - 0.1 * vel[k]
        opt.step(p, g)
    assert all(np.allclose(p[k], ref[k]) for k in p)


def test_adam_matches_reference():
    p = _params()
    ref = {k: v.copy() for k, v in p.items()}
    opt = sub.Adam(0.01, weight_decay=0.1)
    m = {k: 0.0 for k in p}
    v = {k: 0.0 for k in p}
    for t in range(1, 6):
        g = _grads(p)
        lr = 0.003 if t == 3 else 0.01
        for k in ref:
            m[k] = 0.9 * m[k] + 0.1 * g[k]
            v[k] = 0.999 * v[k] + 0.001 * g[k] ** 2
            if k.startswith("W"):
                ref[k] = ref[k] - lr * 0.1 * ref[k]
            ref[k] = ref[k] - lr * (m[k] / (1 - 0.9 ** t)) / (np.sqrt(v[k] / (1 - 0.999 ** t)) + 1e-8)
        opt.step(p, g, lr=0.003 if t == 3 else None)
    assert all(np.allclose(p[k], ref[k]) for k in p)


def test_decoupled_versus_l2():
    zeros = {"W1": np.zeros((3, 2)), "b1": np.zeros(2)}
    p = {"W1": np.full((3, 2), 2.0), "b1": np.full(2, 2.0)}
    opt = sub.Adam(0.01, weight_decay=0.1, decoupled=True)
    for _ in range(10):
        opt.step(p, zeros)
    assert np.allclose(p["W1"], 2.0 * (1 - 0.001) ** 10) and np.allclose(p["b1"], 2.0)
    q = {"W1": np.full((3, 2), 2.0), "b1": np.full(2, 2.0)}
    sub.Adam(0.01, weight_decay=0.1, decoupled=False).step(q, zeros)
    assert np.allclose(q["W1"], 2.0 - 0.01, atol=1e-8)
