import numpy as np
import sub

N = np.array([1e7, 3e7, 1e8, 3e8, 1e9, 1e7, 1e9])
D = np.array([1e9, 3e9, 1e10, 3e10, 1e11, 1e11, 1e9])
truth = np.array([np.log(406.4), np.log(410.7), np.log(1.69), 0.34, 0.28])


def L_of(theta):
    a, b, e, al, be = theta
    return np.exp(e) + np.exp(a) * N ** -al + np.exp(b) * D ** -be


def test_huber():
    v, d = sub.huber(np.array([-2.0, -0.5, 0.0, 0.5, 2.0]), 1.0)
    assert np.allclose(v, [1.5, 0.125, 0, 0.125, 1.5])
    assert np.allclose(d, [-1, -0.5, 0, 0.5, 1])


def test_zero_at_the_true_parameters():
    value, grad = sub.hoffmann_objective(truth, N, D, L_of(truth))
    assert value < 1e-20 and np.allclose(grad, 0, atol=1e-12)


def test_grad_hoffmann_objective():
    L = L_of(truth) * np.exp(np.array([0.02, -0.03, 0.0005, 0.04, -0.01, 0.0002, -0.05]))
    theta = truth + np.array([0.1, -0.2, 0.05, 0.01, -0.02])
    _, g = sub.hoffmann_objective(theta, N, D, L)
    num = []
    for i in range(5):
        e = np.zeros(5)
        e[i] = 1e-6
        num.append((sub.hoffmann_objective(theta + e, N, D, L)[0] - sub.hoffmann_objective(theta - e, N, D, L)[0]) / 2e-6)
    assert np.allclose(g, num, rtol=1e-5, atol=1e-10)
