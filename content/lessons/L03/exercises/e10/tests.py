import numpy as np
import sub

rng = np.random.default_rng(10)
A = rng.normal(size=(2, 6))
x = rng.normal(size=6)
y = np.tanh(A @ x)
D = 1 - y ** 2
J_true = D[:, None] * A
calls = {"jvp": 0, "vjp": 0}


def jvp(v):
    calls["jvp"] += 1
    return D * (A @ v)


def vjp(u):
    calls["vjp"] += 1
    return A.T @ (D * u)


def test_forward_mode_jacobian():
    calls["jvp"] = 0
    J, passes = sub.jacobian_forward(jvp, 6)
    assert np.allclose(J, J_true)
    assert passes == 6 and calls["jvp"] == 6


def test_reverse_mode_jacobian():
    calls["vjp"] = 0
    J, passes = sub.jacobian_reverse(vjp, 2)
    assert np.allclose(J, J_true)
    assert passes == 2 and calls["vjp"] == 2


def test_choice_of_mode():
    assert sub.cheaper_mode(10 ** 9, 1) == "reverse", "a scalar loss of many parameters"
    assert sub.cheaper_mode(1, 1000) == "forward"
    assert sub.cheaper_mode(5, 5) == "either"
