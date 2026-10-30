import sub

S = sub.two_dice()
SUM7 = {w for w in S if sum(w) == 7}
SUM8 = {w for w in S if sum(w) == 8}
FIRST6 = {w for w in S if w[0] == 6}


def test_probabilities():
    assert abs(sub.prob(S, set(S)) - 1) < 1e-12
    assert abs(sub.prob(S, SUM7) - 1 / 6) < 1e-12
    assert abs(sub.prob(S, {w for w in S if 6 in w}) - 11 / 36) < 1e-12


def test_conditioning_and_independence():
    assert abs(sub.conditional(S, FIRST6, SUM7) - 1 / 6) < 1e-12
    assert sub.independent(S, FIRST6, SUM7)
    assert not sub.independent(S, FIRST6, SUM8)
    try:
        sub.conditional(S, FIRST6, set())
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
