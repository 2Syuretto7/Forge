import sub

E = ("+", ("*", 3, "x"), 2)


def test_numbers_and_names():
    assert sub.evaluate(5, {}) == 5
    assert sub.evaluate("x", {"x": 2.5}) == 2.5


def test_trees():
    assert sub.evaluate(E, {"x": 3}) == 11
    assert sub.evaluate(("^", ("-", "a", "b"), 2), {"a": 5, "b": 2}) == 9
    assert abs(sub.evaluate(("/", 1, ("+", "x", "y")), {"x": 1, "y": 3}) - 0.25) < 1e-15


def test_variables():
    assert sub.variables(E) == {"x"}
    assert sub.variables(("*", ("+", "a", "b"), ("-", "c", 1))) == {"a", "b", "c"}
    assert sub.variables(7) == set()
