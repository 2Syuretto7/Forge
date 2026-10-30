import sub


def test_low_degree_both_fine():
    en, eq = sub.coef_errors(3)
    assert en < 1e-8 and eq < 1e-10


def test_qr_wins_at_high_degree():
    en, eq = sub.coef_errors(12)
    assert eq < 1e-4, f"QR error {eq:.2e}"
    assert en > 100 * eq, f"normal {en:.2e} vs QR {eq:.2e}"


def test_sweep_shape():
    s = sub.sweep(6)
    assert [d for d, _, _ in s] == [1, 2, 3, 4, 5, 6]
