import sub


def test_xor():
    S, E = sub.space(), sub.events()
    assert sub.pairwise_independent(S, E)
    assert not sub.mutually_independent(S, E)
