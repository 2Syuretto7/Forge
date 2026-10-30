import itertools
import sub


def test_counts():
    assert sub.full_houses() == 3744
    assert sub.flushes() == 5108
    assert sub.two_pairs() == 123552
    assert abs(sub.probability(3744) - 0.0014405762304921968) < 1e-15


def test_method_on_a_small_deck():
    # 6 ranks, 4 suits: count full houses by brute force and by the same staged formula.
    deck = [(r, s) for r in range(6) for s in range(4)]
    brute = 0
    for hand in itertools.combinations(deck, 5):
        counts = sorted([sum(1 for c in hand if c[0] == r) for r in range(6)], reverse=True)
        brute += counts[:2] == [3, 2]
    assert brute == 6 * 4 * 5 * 6
