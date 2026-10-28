import sub

GB80 = 80 * 2 ** 30


def test_small_model_needs_nothing():
    p = sub.find_plan("1.3B", 8, GB80)
    assert (p["tp"], p["pp"], p["dp"], p["zero"], p["checkpoint"]) == (1, 1, 8, 0, False)


def test_thirteen_billion():
    p = sub.find_plan("13B", 64, GB80)
    assert (p["tp"], p["pp"], p["zero"], p["checkpoint"]) == (1, 1, 1, False)
    q = sub.find_plan("13B", 8, GB80)
    assert q["zero"] >= 1 and q["bytes"] <= 0.9 * GB80


def test_seventy_billion():
    p = sub.find_plan("70B", 64, GB80)
    assert p["zero"] == 3 and p["bytes"] <= 0.9 * GB80
    assert sub.find_plan("70B", 16, 40 * 2 ** 30) is None
