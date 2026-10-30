import sub

EULER = lambda n: n * n + n + 41


def test_is_prime():
    assert [n for n in range(30) if sub.is_prime(n)] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert sub.is_prime(1601) and not sub.is_prime(1681)


def test_euler():
    assert sub.first_composite(EULER) == 40
    assert sub.factor_pair(EULER(40)) == (41, 41)
    assert sub.prime_count(EULER, 10000) == 4149


def test_mersenne_and_fermat():
    # 2^p - 1 for prime p: prime for p = 2, 3, 5, 7, then 2047 = 23 x 89 at p = 11.
    assert sub.factor_pair(2 ** 11 - 1) == (23, 89)
    # Fermat guessed 2^(2^n) + 1 is always prime; n = 5 gives 641 x 6700417.
    assert sub.factor_pair(2 ** 32 + 1) == (641, 6700417)
