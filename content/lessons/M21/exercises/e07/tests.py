import sub


def test_monty():
    assert abs(sub.bayes_switch_win() - 2 / 3) < 1e-12
    assert abs(sub.simulate(30000, True) - 2 / 3) < 0.015
    assert abs(sub.simulate(30000, False) - 1 / 3) < 0.015
