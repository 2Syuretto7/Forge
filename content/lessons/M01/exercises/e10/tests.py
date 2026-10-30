import math
import sub


def test_tokens_for():
    assert sub.tokens_for(1e8) == 2e9
    assert sub.tokens_for(7e9, 286) == 7e9 * 286


def test_gpu_hours():
    assert math.isclose(sub.gpu_hours(1e8, 2e9, 1e14, utilization=1.0), 1.2e18 / 1e14 / 3600, rel_tol=1e-12)
    assert math.isclose(sub.gpu_hours(1e8, 2e9, 1e14), 1.2e18 / 4e13 / 3600, rel_tol=1e-12)


def test_a_seven_billion_model():
    # 7e9 parameters on 2e12 tokens at 1e15 FLOP/s and 40% utilization: about 58,000 GPU-hours.
    h = sub.gpu_hours(7e9, 2e12, 1e15)
    assert math.isclose(h, 8.4e22 / 4e14 / 3600, rel_tol=1e-12)
    assert 5e4 < h < 7e4
    days = sub.wall_clock_days(h, 1024)
    assert math.isclose(days, h / 1024 / 24, rel_tol=1e-12) and 2 < days < 3


def test_cost():
    assert sub.run_cost(100, 2.5) == 250
