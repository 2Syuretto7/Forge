import numpy as np
import sub

rng = np.random.default_rng(7)
Z = rng.normal(size=(6, 4)) * 3
Y = rng.integers(0, 4, size=6)


def _ref(Z, y):
    m = Z.max(axis=1, keepdims=True)
    lse = (m + np.log(np.exp(Z - m).sum(axis=1, keepdims=True)))[:, 0]
    return float(np.mean(lse - Z[np.arange(len(y)), y]))


def _num(f, x, h=1e-6):
    g = np.zeros_like(x)
    for idx in np.ndindex(x.shape):
        e = np.zeros_like(x)
        e[idx] = h
        g[idx] = (f(x + e) - f(x - e)) / (2 * h)
    return g


def test_values():
    for fn in (sub.cross_entropy, sub.cross_entropy_fused):
        assert abs(float(fn(sub.Tensor(Z), Y).data) - _ref(Z, Y)) < 1e-10


def test_grad_composite():
    t = sub.Tensor(Z)
    sub.cross_entropy(t, Y).backward()
    assert np.allclose(t.grad, _num(lambda x: _ref(x, Y), Z), atol=1e-6)


def test_grad_fused_matches_composite():
    a, b = sub.Tensor(Z), sub.Tensor(Z)
    sub.cross_entropy(a, Y).backward()
    sub.cross_entropy_fused(b, Y).backward()
    assert np.allclose(a.grad, b.grad, atol=1e-12)


def test_fused_is_one_node():
    t = sub.Tensor(Z)
    out = sub.cross_entropy_fused(t, Y)
    assert len(out._parents) == 1 and out._parents[0] is t


def test_stable_for_large_logits():
    t = sub.Tensor(Z * 300)
    v = float(sub.cross_entropy(t, Y).data)
    assert np.isfinite(v) and abs(v - _ref(Z * 300, Y)) < 1e-8
