import numpy as np
import sub

rng = np.random.default_rng(8)
x = rng.normal(size=7) * 2 + 1


def test_output_is_normalized():
    y = sub.layernorm(x, 0.0)
    assert abs(y.mean()) < 1e-12 and abs(np.mean(y ** 2) - 1) < 1e-12


def test_grad_vjp_matches_finite_differences():
    for eps in [0.0, 1e-3]:
        u = rng.normal(size=7)
        g = sub.layernorm_vjp(x, u, eps)
        num = np.zeros(7)
        for j in range(7):
            e = np.zeros(7)
            e[j] = 1e-6
            num[j] = (u @ sub.layernorm(x + e, eps) - u @ sub.layernorm(x - e, eps)) / 2e-6
        assert np.linalg.norm(g - num) / (np.linalg.norm(g) + np.linalg.norm(num)) < 1e-5


def test_shift_invariance():
    J = sub.layernorm_jacobian(x, 1e-3)
    assert np.allclose(J @ np.ones(7), 0, atol=1e-12)


def test_scale_invariance_without_epsilon():
    J = sub.layernorm_jacobian(x, 0.0)
    assert np.allclose(J @ x, 0, atol=1e-12)
