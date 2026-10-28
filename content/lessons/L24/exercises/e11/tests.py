import sub

train = ["REVERSE: apple", "UPPER: pear", "REVERSE: stone", "UPPER: night"]
evals = ["upper:  PEAR", "REVERSE: river", "REVERSE: stone", "UPPER: cloud", "UPPER: light"]


def test_leaks():
    assert sub.leaked_items(evals, train) == [0, 2]


def test_honest():
    acc = sub.honest_accuracy([1, 0, 1, 1, 0], [0, 2])
    assert acc["all"] == 0.6 and abs(acc["clean"] - 1 / 3) < 1e-12 and acc["leaked"] == 1.0
    assert sub.honest_accuracy([1, 0], [])["leaked"] is None
