from fractions import Fraction
import sub


def test_two_dice():
    S = sub.dice_space(2)
    assert len(S) == 36
    assert sub.probability(lambda w: sum(w) == 7, S) == Fraction(1, 6)
    assert sub.probability(lambda w: w[0] == w[1], S) == Fraction(1, 6)


def test_complement_and_at_least_one():
    S = sub.dice_space(4)
    six = lambda w: 6 in w
    assert sub.probability(six, S) == sub.p_at_least_one_six(4) == Fraction(671, 1296)
    assert sub.probability(sub.complement(six), S) == 1 - sub.probability(six, S)
