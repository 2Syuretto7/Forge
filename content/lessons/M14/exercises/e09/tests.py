import numpy as np
import sub

rng = np.random.default_rng(9)


def test_invariant_norms():
    for _ in range(50):
        m, n = rng.integers(1, 9, size=2)
        A = rng.normal(size=(m, n))
        f = sub.frobenius_from_s(A)
        s1 = sub.spectral_norm(A)
        assert np.isclose(f, np.sqrt(np.sum(A * A)))
        assert sub.stretch_samples(A) <= s1 * (1 + 1e-12)
        r = min(m, n)
        assert s1 <= f + 1e-12 <= np.sqrt(r) * s1 + 2e-12


def test_samples_get_close():
    A = np.diag([3.0, 1.0])
    assert sub.stretch_samples(A) > 2.99
