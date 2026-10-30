import sub


def test_standard_error():
    assert abs(sub.standard_error(0.5, 100) - 0.05) < 1e-15


def test_simulation_agrees():
    est = sub.simulate(sub.roll_two_sum_seven, 20000)
    assert abs(sub.z_score(est, 1 / 6, 20000)) < 3.5


def test_reproducible():
    assert sub.simulate(sub.roll_two_sum_seven, 1000, 5) == sub.simulate(sub.roll_two_sum_seven, 1000, 5)
