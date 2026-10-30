import sub


def test_strings():
    assert sub.count_strings(26, 4) == 456976
    assert sub.count_distinct_strings(26, 4) == 358800
    assert sub.count_distinct_strings(3, 4) == 0
    assert sub.count_strings(2, 10) == 1024


def test_rules():
    assert sub.count_either(3, 4, 5) == 12
    assert sub.count_staged(3, 4, 5) == 60
    assert sub.count_staged() == 1
