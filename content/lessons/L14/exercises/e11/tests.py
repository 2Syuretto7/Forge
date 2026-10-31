import sub

NAN = float("nan")


def test_simulator():
    assert sub.run_collectives([["a", "b"], ["a", "b"]]) == ("ok", 2)
    assert sub.run_collectives([["a", "b"], ["a", "c"]]) == ("mismatch", 1, ["b", "c"])
    assert sub.run_collectives([["a"], ["a", "b"], ["a", "b"]]) == ("hang", 1, [1, 2])


def test_nan_on_one_rank():
    losses = [[1.0, 0.9, 0.8], [1.0, NAN, 0.8], [1.0, 0.9, 0.8]]
    bad = sub.run_collectives(sub.training_trace(losses, consensus=False))
    assert bad[0] == "hang"
    good = sub.run_collectives(sub.training_trace(losses, consensus=True))
    assert good == ("ok", 3 + 2)
