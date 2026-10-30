from fractions import Fraction as Fr

import sub


def test_polynomial_helpers():
    p = [Fr(1), Fr(2), Fr(3)]  # 1 + 2n + 3n^2
    assert sub.peval(p, 2) == 17
    assert sub.pequal(sub.pshift(p), [Fr(6), Fr(8), Fr(3)])
    assert sub.pequal(sub.pmul([1, 1], [1, -1]), [1, 0, -1])
    assert sub.pequal(sub.padd(p, sub.pscale(p, -1)), [])


def test_sum_of_squares_is_proved():
    f = [0, 0, 1]  # k^2
    F = [Fr(0), Fr(1, 6), Fr(1, 2), Fr(1, 3)]  # n/6 + n^2/2 + n^3/3
    assert sub.induction_check(f, F) == (True, True)


def test_sum_of_odds_is_proved():
    assert sub.induction_check([-1, 2], [0, 0, 1]) == (True, True)


def test_a_fitted_guess_fails_the_step():
    # F(n) = n^2 matches the sum of squares at n = 1, and nowhere else that matters.
    assert sub.induction_check([0, 0, 1], [0, 0, 1]) == (True, False)
