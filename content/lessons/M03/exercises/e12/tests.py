import sub


def test_sieve():
    assert sub.sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(sub.sieve(10000)) == 1229


def test_race():
    assert sub.race(100) == (11, 13)
    assert sub.race(26861) == (1473, 1472)


def test_the_lead_changes_late():
    assert sub.first_lead_change(26000) is None
    assert sub.first_lead_change(30000) == 26861
