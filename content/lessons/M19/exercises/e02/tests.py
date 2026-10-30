import sub


def test_reuse():
    x = sub.Var(2.0)
    y = x
    for _ in range(9):
        y = y + x
    order = sub.topo_order(y)
    assert order[-1] is y and sum(1 for v in order if v is x) == 1
    assert sub.is_valid_order(order)
    assert not sub.is_valid_order(order[::-1])


def test_ladder():
    x = sub.Var(1.0)
    v = x
    for _ in range(30):
        v = v * 1.0 + v * 1.0
    assert sub.count_paths(v, x) == 2 ** 30
    order = sub.topo_order(v)
    assert len(order) < 200 and sub.is_valid_order(order)
