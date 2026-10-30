import numpy as np
import sub

rng = np.random.default_rng(14)


def test_singular_values_two_ways():
    A = sub.ill_matrix(1e10)
    a, b = sub.smallest_two_ways(A)
    assert abs(a / 1e-10 - 1) < 1e-3, f"SVD gave {a:.3e}"
    assert not (1e-11 < b < 1e-9), f"the Gram route should be off by more than a factor of 10, gave {b:.3e}"
    a, b = sub.smallest_two_ways(sub.ill_matrix(1e3))
    assert abs(b / a - 1) < 1e-6


def test_qr_beats_normal_equations():
    out = sub.normal_vs_qr(sub.ill_matrix(1e6), rng.normal(size=6))
    assert out["qr"] < 1e-7, f"QR error {out['qr']:.2e}"
    assert out["normal"] > 100 * out["qr"]
