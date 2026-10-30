import sub


def test_formula_matches_measurement():
    for n in [10, 100, 625]:
        assert abs(sub.sqrt_error(n) - sub.predicted_sqrt_error(n)) < 2e-4


def test_square_root_law():
    # Four times the pieces only halves the error: exponent 1/2, not 2.
    r = sub.sqrt_error(100) / sub.sqrt_error(400)
    assert 1.8 < r < 2.2, r


def test_pieces_for_sqrt():
    assert sub.pieces_for_sqrt(0.01) == 625
    assert sub.pieces_for_sqrt(0.05) == 25
