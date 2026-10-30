import sub


def test_survival_times():
    t = sub.survival_times(sub.RESULTS)
    assert t == [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4, 6, 7, 7, 8, 10, 17, 20, 41, 42]


def test_median():
    assert sub.median([1, 2, 3]) == 2
    assert sub.median([1, 2, 3, 10]) == 2.5
    assert sub.median(sub.survival_times(sub.RESULTS)) == 4


def test_long_tail():
    assert sub.longest_survivor(sub.RESULTS) == "n^2 - n + 41 is prime"
    assert sub.share_within(sub.RESULTS, 10) > 0.8
    assert sub.share_within(sub.RESULTS, 30) < 1
