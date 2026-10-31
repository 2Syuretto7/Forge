import numpy as np
import sub

rng = np.random.default_rng(11)


def test_mul_inplace():
    t = sub.Tensor(np.array([1.0, 2.0]))
    sub.mul_(t, 3.0)
    sub.mul_(t, 0.5)
    assert np.allclose(t.data, [1.5, 3.0]) and t._version == 2


def test_grad_checked_mul_normal_use():
    a, b = sub.Tensor(rng.normal(size=(3, 2))), sub.Tensor(rng.normal(size=2))
    sub.checked_mul(a, b).sum().backward()
    assert np.allclose(a.grad, np.tile(b.data, (3, 1)))
    assert np.allclose(b.grad, a.data.sum(axis=0))


def test_unprotected_gives_wrong_gradient():
    x, w = sub.Tensor(np.array([1.0, 2.0])), sub.Tensor(np.array([3.0, 4.0]))
    loss = (x * w).sum()
    x.data *= 2  # the bug: the gradient of w is the original x
    loss.backward()
    assert np.allclose(w.grad, [2.0, 4.0])  # wrong, silently


def test_checked_raises_after_inplace():
    x, w = sub.Tensor(np.array([1.0, 2.0])), sub.Tensor(np.array([3.0, 4.0]))
    loss = sub.checked_mul(x, w).sum()
    sub.mul_(x, 2.0)
    try:
        loss.backward()
    except RuntimeError:
        return
    raise AssertionError("backward used a tensor modified in place without raising")


def test_unrelated_inplace_is_fine():
    x, w, z = (sub.Tensor(np.array([1.0, 2.0])) for _ in range(3))
    loss = sub.checked_mul(x, w).sum()
    sub.mul_(z, 5.0)
    loss.backward()
    assert np.allclose(w.grad, x.data)
