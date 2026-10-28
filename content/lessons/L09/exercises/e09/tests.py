import numpy as np
import sub

X, y = sub.make_digits(8, 3)


def test_l2_value():
    p = sub.init([64, 6, 5, 10], seed=1)
    base, _ = sub.loss_and_grads(p, X, y)
    pen, _ = sub.loss_and_grads_l2(p, X, y, 0.3)
    expect = 0.15 * sum(np.sum(p[k] ** 2) for k in p if k.startswith("W"))
    assert abs(pen - base - expect) < 1e-10


def test_grad_l2():
    p = sub.init([64, 6, 5, 10], seed=2)
    p["b1"] += 0.1
    _, g = sub.loss_and_grads_l2(p, X, y, 0.3)
    for k in ["W1", "b1", "W2", "b3"]:
        num = np.zeros_like(p[k])
        for idx in np.ndindex(p[k].shape):
            old = p[k][idx]
            p[k][idx] = old + 1e-6
            lp, _ = sub.loss_and_grads_l2(p, X, y, 0.3)
            p[k][idx] = old - 1e-6
            lm, _ = sub.loss_and_grads_l2(p, X, y, 0.3)
            p[k][idx] = old
            num[idx] = (lp - lm) / 2e-6
        assert np.allclose(g[k], num, atol=1e-6), k


def test_global_norm():
    g = {"a": np.array([3.0, 0.0]), "b": np.array([[4.0]])}
    assert abs(sub.global_norm(g) - 5.0) < 1e-12


def test_clip():
    g = {"a": np.array([3.0, 0.0]), "b": np.array([[4.0]])}
    c = sub.clip_by_global_norm(g, 1.0)
    assert abs(sub.global_norm(c) - 1.0) < 1e-12
    assert np.allclose(c["a"], [0.6, 0.0]) and np.allclose(c["b"], [[0.8]])
    assert np.allclose(g["a"], [3.0, 0.0])
    same = sub.clip_by_global_norm(g, 10.0)
    assert np.allclose(same["a"], g["a"]) and np.allclose(same["b"], g["b"])
