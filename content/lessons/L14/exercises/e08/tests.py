import sub


def test_orders():
    assert sub.gpipe_order(2, 2)[0] == [("F", 0), ("F", 1), ("B", 1), ("B", 0)]
    o = sub.one_f_one_b_order(3, 4)
    assert o[0] == [("F", 0), ("F", 1), ("F", 2), ("B", 0), ("F", 3), ("B", 1), ("B", 2), ("B", 3)]
    assert o[2] == [("F", 0), ("B", 0), ("F", 1), ("B", 1), ("F", 2), ("B", 2), ("F", 3), ("B", 3)]


def test_time_and_memory():
    for p, m in [(4, 8), (4, 4), (2, 6), (8, 32)]:
        tg, mg = sub.simulate(sub.gpipe_order(p, m))
        t1, m1 = sub.simulate(sub.one_f_one_b_order(p, m))
        assert tg == t1 == (m + p - 1) * 3.0
        assert mg == m and m1 == min(p, m)
