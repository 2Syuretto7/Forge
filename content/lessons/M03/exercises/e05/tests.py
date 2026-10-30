import sub

SQ = [(-1, 1), (0, 0), (1, 1)]


def test_is_function():
    assert sub.is_function(SQ, [-1, 0, 1])
    assert not sub.is_function([(0, 0), (0, 1), (1, 1)], [0, 1])
    assert not sub.is_function([(0, 0)], [0, 1])


def test_properties():
    assert sub.apply(SQ, -1) == 1
    assert not sub.is_injective(SQ)
    assert sub.is_injective([(0, "a"), (1, "b")])
    assert sub.is_surjective(SQ, [0, 1]) and not sub.is_surjective(SQ, [0, 1, 2])


def test_compose():
    inc = [(0, 1), (1, 2), (-1, 0)]
    assert sorted(sub.compose(inc, SQ)) == [(-1, 2), (0, 1), (1, 2)]


def test_count_functions():
    fs = sub.all_functions(["a", "b", "c"], [0, 1])
    assert len(fs) == 8
    assert all(sub.is_function(f, ["a", "b", "c"]) for f in fs)
    assert len(sub.all_functions([1, 2], ["x", "y", "z"])) == 9
    assert sum(sub.is_injective(f) for f in sub.all_functions([1, 2], [0, 1, 2])) == 6
