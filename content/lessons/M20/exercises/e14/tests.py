import sub


def test_signs():
    assert sub.signed_density(2.0) < 0 and sub.density(2.0) == 0.25


def test_grad_density_is_minus_tail_derivative():
    h = 1e-6
    for y in (1.5, 4.0, 20.0):
        assert abs(-(sub.prob_greater(y + h) - sub.prob_greater(y - h)) / (2 * h) - sub.density(y)) < 1e-7


def test_probability():
    n, a, b = 200_000, 3.0, 3000.0
    h = (b - a) / n
    approx = sum(sub.density(a + h * (k + 0.5)) for k in range(n)) * h
    assert abs(approx - (sub.prob_greater(a) - sub.prob_greater(b))) < 1e-6
