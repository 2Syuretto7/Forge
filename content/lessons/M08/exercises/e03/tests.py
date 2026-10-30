import sub


def test_values():
    assert sub.comb_factorial(5, 2) == 10
    assert sub.comb_pascal(52, 5) == 2598960
    assert sub.comb_multiplicative(200, 100) == 90548514656103281165404177077484163874504589675413336841320
    assert sub.comb_multiplicative(5, 7) == 0


def test_invariant_three_ways_agree():
    for n in range(41):
        for k in range(n + 1):
            a = sub.comb_factorial(n, k)
            assert a == sub.comb_pascal(n, k) == sub.comb_multiplicative(n, k), (n, k)
            assert a == sub.comb_factorial(n, n - k)
