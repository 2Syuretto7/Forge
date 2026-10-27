import numpy as np
import sub

rng = np.random.default_rng(4)
A = rng.normal(size=(3, 5))


def test_linear_map_has_constant_jacobian():
    J = sub.numerical_jacobian(lambda x: A @ x, rng.normal(size=5))
    assert J.shape == (3, 5)
    assert np.allclose(J, A, atol=1e-8)


def test_elementwise_function_has_diagonal_jacobian():
    x = rng.normal(size=4)
    J = sub.numerical_jacobian(np.tanh, x)
    assert np.allclose(J, np.diag(1 - np.tanh(x) ** 2), atol=1e-8)


def test_example_from_the_derivation():
    f = lambda x: np.array([x[0] * x[1], np.sin(x[0])])  # noqa: E731
    J = sub.numerical_jacobian(f, np.array([0.5, 3.0]))
    assert np.allclose(J, [[3.0, 0.5], [np.cos(0.5), 0.0]], atol=1e-8)


def test_chain_rule():
    B = rng.normal(size=(2, 3))
    x = rng.normal(size=5)
    f = lambda v: np.tanh(A @ v)  # noqa: E731
    g = lambda y: B @ (y ** 2)  # noqa: E731
    Jf = sub.numerical_jacobian(f, x)
    Jg = sub.numerical_jacobian(g, f(x))
    Jgf = sub.numerical_jacobian(lambda v: g(f(v)), x)
    assert np.allclose(sub.jacobian_of_composition(Jg, Jf), Jgf, atol=1e-7)
