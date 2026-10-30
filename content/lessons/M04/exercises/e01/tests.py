import sub


def test_machines():
    assert sub.square(-3) == 9
    assert sub.relu(-2) == 0 and sub.relu(2.5) == 2.5


def test_affine_returns_a_function():
    f = sub.affine(3, 2)
    assert callable(f), "affine should return a function"
    assert f(4) == 14 and f(0) == 2
    g = sub.affine(-1, 0)
    assert g(5) == -5 and f(1) == 5, "each machine keeps its own a and b"


def test_apply_all():
    assert sub.apply_all(sub.relu, [-1, 0, 2]) == [0, 0, 2]
