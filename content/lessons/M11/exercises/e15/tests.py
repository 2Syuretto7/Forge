import numpy as np
import sub

rng = np.random.default_rng(0)


def test_amplification():
    assert abs(sub.amplification(1e-3, 1e-6) / (np.sqrt(2) / 1e-3) - 1) < 1e-3
    A, b = sub.system(1e-3)
    assert abs(sub.cond_inf(A) - (2.001 ** 2) / 1e-3) < 1e-6 * 4000


def test_invariant_perturbation_bound():
    inf = lambda v: np.max(np.abs(v))
    for delta in [1e-1, 1e-3, 1e-6]:
        A, b = sub.system(delta)
        x = np.linalg.solve(A, b)
        k = sub.cond_inf(A)
        for _ in range(50):
            db = 1e-8 * rng.normal(size=2)
            dx = np.linalg.solve(A, b + db) - x
            assert inf(dx) / inf(x) <= k * inf(db) / inf(b) * (1 + 1e-6) + 1e-15
