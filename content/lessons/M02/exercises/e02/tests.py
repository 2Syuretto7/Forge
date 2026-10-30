import sub


def test_to_string():
    assert sub.to_string(("+", ("*", 3, "x"), 2)) == "((3 * x) + 2)"
    assert sub.to_string(("-", ("-", "a", "b"), "c")) == "((a - b) - c)"
    assert sub.to_string(("-", "a", ("-", "b", "c"))) == "(a - (b - c))"
    assert sub.to_string("y") == "y" and sub.to_string(2.5) == "2.5"


def test_counts():
    e = ("/", ("+", "x", 1), ("^", "x", 2))
    assert sub.count_operations(e) == 3
    assert sub.depth(e) == 2
    assert sub.depth(7) == 0 and sub.count_operations("x") == 0
