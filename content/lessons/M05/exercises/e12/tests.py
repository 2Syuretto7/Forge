import sub


def test_remainder_matches_the_sum():
    r, n = 0.7, 12
    s = sum(r ** k for k in range(n))
    assert abs(1 / (1 - r) - s - sub.remainder(r, n)) < 1e-12


def test_terms_needed():
    for r, eps in [(0.5, 1e-6), (0.9, 1e-6), (0.99, 1e-3)]:
        n = sub.terms_needed(r, eps)
        assert sub.remainder(r, n) < eps <= sub.remainder(r, n - 1)
    assert sub.terms_needed(0.5, 1e-6) == 21


def test_closer_to_one_costs_more():
    ratio = sub.work_ratio(0.9, 0.99, 1e-6)
    assert 8 < ratio < 14, ratio
