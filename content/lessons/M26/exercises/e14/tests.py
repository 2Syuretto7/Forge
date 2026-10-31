import numpy as np
import sub


def test_failure_points():
    g32 = sub.first_failure(np.float32)
    g64 = sub.first_failure(np.float64)
    assert 100 <= g32 <= 106 and 740 <= g64 <= 750, (g32, g64)


def test_logits_version_survives():
    for dtype, g in ((np.float32, 200.0), (np.float64, 1000.0)):
        z = np.array([g, 0.0], dtype=dtype)
        assert sub.ce_from_probs(z, 1) == np.inf
        assert abs(sub.ce_from_logits(z, 1) - g) < 1e-3
        assert abs(sub.ce_from_logits(z, 0)) < 1e-6


def test_agree_when_safe():
    z = np.array([2.0, -1.0, 0.5])
    assert abs(sub.ce_from_probs(z, 2) - sub.ce_from_logits(z, 2)) < 1e-12
