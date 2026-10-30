import sub


def test_invariant_matches_brute_force():
    for n in range(0, 200):
        assert sub.sum_first(n) == sum(range(n + 1))
        assert sub.sum_odds(n) == sum(range(1, 2 * n, 2))
        assert sub.sum_squares(n) == sum(k * k for k in range(n + 1))
        assert sub.sum_cubes(n) == sum(k ** 3 for k in range(n + 1))


def test_big_and_exact():
    assert sub.sum_first(10 ** 12) == 500000000000500000000000
    assert isinstance(sub.sum_squares(10 ** 6), int)
