import numpy as np
import sub

rng = np.random.default_rng(8)


def test_parameters_found():
    m = sub.MLP([3, 5, 4, 2], seed=1)
    ps = m.parameters()
    assert [p.shape for p in ps] == [(3, 5), (5,), (5, 4), (4,), (4, 2), (2,)]
    assert all(getattr(p, "is_param", False) for p in ps)


def test_he_init_scale():
    lin = sub.Linear(400, 300, np.random.default_rng(0))
    assert abs(lin.W.data.std() - np.sqrt(2 / 400)) < 0.003
    assert np.all(lin.b.data == 0)


def test_forward_relu_between_layers():
    m = sub.MLP([3, 6, 2], seed=2)
    X = rng.normal(size=(4, 3))
    W1, b1, W2, b2 = (p.data for p in m.parameters())
    ref = np.maximum(X @ W1 + b1, 0) @ W2 + b2
    assert np.allclose(m(sub.Tensor(X)).data, ref)


def test_grad_mlp():
    m = sub.MLP([3, 6, 2], seed=3)
    X = rng.normal(size=(5, 3))
    G = rng.normal(size=(5, 2))
    (m(sub.Tensor(X)) * sub.Tensor(G)).sum().backward()
    for p in m.parameters():
        num = np.zeros_like(p.data)
        for idx in np.ndindex(p.shape):
            old = p.data[idx]
            p.data[idx] = old + 1e-6
            fp = np.sum(G * m(sub.Tensor(X)).data)
            p.data[idx] = old - 1e-6
            fm = np.sum(G * m(sub.Tensor(X)).data)
            p.data[idx] = old
            num[idx] = (fp - fm) / 2e-6
        assert np.allclose(p.grad, num, atol=1e-6)


def test_sgd_and_zero_grad():
    m = sub.MLP([2, 3, 1], seed=4)
    opt = sub.SGD(m.parameters(), 0.1)
    before = [p.data.copy() for p in m.parameters()]
    ids = [id(p) for p in m.parameters()]
    (m(sub.Tensor(rng.normal(size=(4, 2)))) ** 2).sum().backward()
    grads = [p.grad.copy() for p in m.parameters()]
    opt.step()
    for p, b, g in zip(m.parameters(), before, grads):
        assert np.allclose(p.data, b - 0.1 * g)
    assert [id(p) for p in m.parameters()] == ids
    opt.zero_grad()
    assert all(p.grad is None for p in m.parameters())
    m.zero_grad()
    assert all(p.grad is None for p in m.parameters())
