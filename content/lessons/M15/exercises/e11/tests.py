import numpy as np
import sub


def test_grad_vectorized():
    x = np.linspace(0.1, 3, 100)
    assert np.allclose(sub.central_vec(np.sin, x, 1e-5), np.cos(x), atol=1e-9)


def test_compare():
    fixed, scaled = sub.compare_steps(200_000)
    assert fixed > 1e-5, fixed
    assert scaled < 1e-8, scaled
