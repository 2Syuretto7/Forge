import numpy as np
import sub


def test_matvec_values_and_count():
    rng = np.random.default_rng(0)
    for m, n in [(3, 4), (7, 2), (1, 9)]:
        W = rng.normal(size=(m, n))
        x = rng.normal(size=n)
        y, flops = sub.matvec(W.tolist(), x.tolist())
        assert np.allclose(y, W @ x, atol=1e-12)
        assert flops == 2 * m * n, f"{m}x{n}: counted {flops}, expected {2 * m * n}"


def test_mlp():
    assert sub.mlp_flops([784, 512, 10]) == 2 * (784 * 512 + 512 * 10)
    assert sub.mlp_flops([784, 512, 512, 10], batch=64) == 85590016
    assert sub.mlp_params([784, 512, 512, 10]) == 669706


def test_two_flops_per_parameter():
    widths = [1000, 1000, 1000]
    weights = sum(a * b for a, b in zip(widths[:-1], widths[1:]))
    assert sub.mlp_flops(widths) == 2 * weights


def test_train_flops():
    assert sub.train_flops(1e8, 2e9) == 1.2e18
    assert abs(sub.train_flops(7e9, 2e12) / 8.4e22 - 1) < 1e-12
