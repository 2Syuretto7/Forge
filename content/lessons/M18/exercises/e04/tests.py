import numpy as np
import sub

rng = np.random.default_rng(5)


def softmax(z):
    p = np.exp(z - z.max())
    return p / p.sum()


def test_grad_layers():
    W = rng.normal(size=(3, 4))
    x = rng.normal(size=4)
    cases = [
        (sub.jac_affine(W), sub.numerical_jacobian(lambda v: W @ v + 1.0, x)),
        (sub.jac_tanh(x), sub.numerical_jacobian(np.tanh, x)),
        (sub.jac_softmax(x), sub.numerical_jacobian(softmax, x)),
        (sub.jac_normalize(x), sub.numerical_jacobian(lambda v: v / np.linalg.norm(v), x)),
    ]
    v = np.array([1.7, 0.4])
    cases.append((sub.jac_polar(v), sub.numerical_jacobian(lambda q: np.array([q[0] * np.cos(q[1]), q[0] * np.sin(q[1])]), v)))
    for exact, num in cases:
        assert np.allclose(exact, num, atol=1e-8)


def test_structure():
    z = rng.normal(size=5)
    assert np.allclose(sub.jac_softmax(z).sum(axis=0), 0)
    assert np.isclose(np.linalg.det(sub.jac_polar([2.5, 1.0])), 2.5)
    x = rng.normal(size=3)
    assert np.allclose(sub.jac_normalize(x) @ x, 0)
