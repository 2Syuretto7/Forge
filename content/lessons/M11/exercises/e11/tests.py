import sub


def test_small():
    assert sub.lu_flops(2) == 3
    assert sub.lu_flops(3) == 3 + 10
    assert sub.tri_flops(4) == 16


def test_asymptotics():
    assert abs(sub.lu_flops(2000) / (2 * 2000 ** 3 / 3) - 1) < 1e-3


def test_many():
    once = sub.many_rhs_flops(1000, 100, False)
    again = sub.many_rhs_flops(1000, 100, True)
    assert once == sub.lu_flops(1000) + 100 * 2 * 10 ** 6
    assert 76 < again / once < 78
