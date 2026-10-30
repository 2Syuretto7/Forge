import sub


def test_implies():
    assert sub.implies(True, True) and not sub.implies(True, False)
    assert sub.implies(False, True) and sub.implies(False, False)


def test_table_order_and_values():
    t = sub.truth_table(lambda p, q: p and q, 2)
    assert [r for r, _ in t] == [(True, True), (True, False), (False, True), (False, False)]
    assert [v for _, v in t] == [True, False, False, False]
    assert len(sub.truth_table(lambda a, b, c: a, 3)) == 8


def test_count_true():
    assert sub.count_true(sub.implies, 2) == 3
    assert sub.count_true(lambda p, q, r: p or q or r, 3) == 7
