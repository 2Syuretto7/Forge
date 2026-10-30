import sub


def test_invariant_counts_match_formulas():
    for n in [0, 1, 2, 3, 10, 37, 64]:
        assert (sub.count_pairs(n), sub.count_triples(n), sub.count_halvings(n)) == sub.formulas(n), n


def test_values():
    assert sub.formulas(100) == (4950, 161700, 7)
    assert sub.count_halvings(1024) == 11
