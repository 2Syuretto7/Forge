import sub


def test_evaluate_and_agree():
    e = ("+", ("*", 3, "x"), 2)
    assert sub.evaluate(e, {"x": 3}) == 11
    assert sub.agree(("*", "a", ("+", "b", "c")), ("+", ("*", "a", "b"), ("*", "a", "c")), ["a", "b", "c"])
    assert not sub.agree(("^", ("+", "a", "b"), 2), ("+", ("^", "a", 2), ("^", "b", 2)), ["a", "b"])
    assert sub.agree(("/", ("^", "x", 2), "x"), "x", ["x"])


def test_first_bad_step():
    steps = ["x", ("+", "x", 0), ("*", "x", 2), ("*", 2, "x")]
    assert sub.first_bad_step(steps, ["x"]) == 2
    assert sub.first_bad_step(steps[:2], ["x"]) is None


def test_the_notebook():
    assert len(sub.NOTEBOOK) == 15
    found = sub.audit(sub.NOTEBOOK)
    assert found == [(5, 1), (10, 2)], f"audit found {found}"
    titles = [sub.NOTEBOOK[k]["title"] for k, _ in found]
    assert titles == ["Distribute a minus sign", "Square of a difference"]
