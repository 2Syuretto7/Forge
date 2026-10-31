import numpy as np
import sub


def test_accelerates():
    lam = 1e-3
    f, g = sub.ridge_logistic(lam)
    L = np.linalg.eigvalsh(sub.X.T @ sub.X)[-1] / (4 * len(sub.Y)) + lam
    kappa = L / lam
    beta = (np.sqrt(kappa) - 1) / (np.sqrt(kappa) + 1)
    ref = sub.nesterov(g, np.zeros(5), 1 / L, beta, 6000)[-1]
    fs = f(ref)

    def steps(b):
        xs = sub.nesterov(g, np.zeros(5), 1 / L, b, 6000)
        for k, x in enumerate(xs):
            if f(x) - fs < 1e-8:
                return k
        return 6000

    k_nag, k_gd = steps(beta), steps(0.0)
    assert k_gd > 3 * k_nag, (k_gd, k_nag)


def test_gradient_of_ridge_term():
    f, g = sub.ridge_logistic(0.5)
    w = np.array([0.1, 0.2, -0.3, 0.0, 1.0])
    h = 1e-6
    num = np.array([(f(w + h * e) - f(w - h * e)) / (2 * h) for e in np.eye(5)])
    assert np.allclose(num, g(w), atol=1e-7)
