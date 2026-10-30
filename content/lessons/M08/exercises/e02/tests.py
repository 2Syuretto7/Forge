import sub


def test_values():
    assert [sub.factorial(n) for n in range(6)] == [1, 1, 2, 6, 24, 120]
    assert sub.factorial(52) == 80658175170943878571660636856403766975289505440883277824000000000000
    assert sub.arrangements(26, 4) == 358800
    assert sub.arrangements(5, 0) == 1


def test_invariant_permutation_counts():
    for n in range(0, 8):
        items = list(range(n))
        perms = sub.all_permutations(items)
        assert len(perms) == sub.factorial(n)
        assert len({tuple(p) for p in perms}) == len(perms)
        assert all(sorted(p) == items for p in perms)
