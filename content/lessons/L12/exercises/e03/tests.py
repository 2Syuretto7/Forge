import sub


def test_transactions():
    assert [sub.transactions(s) for s in (1, 2, 4, 8, 32)] == [4, 8, 16, 32, 32]
    assert sub.transactions(1, elem_bytes=2) == 2


def test_efficiency():
    assert sub.efficiency(1) == 1.0
    assert sub.efficiency(8) == 0.125
    assert sub.efficiency(2) == 0.5
