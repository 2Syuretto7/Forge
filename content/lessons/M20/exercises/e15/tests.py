import sub


def test_totals():
    assert abs(sub.total_half_open(sub.one_branch) - 0.5) < 1e-6
    assert abs(sub.total_half_open(sub.chi_square_1) - 1) < 1e-6
