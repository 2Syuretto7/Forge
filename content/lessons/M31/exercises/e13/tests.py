import numpy as np
import sub


def test_naive_interval_fails_honest_one_holds():
    rng = np.random.default_rng(14)
    miss, ok = 0, 0
    for _ in range(20):
        rep, lo, hi = sub.select_and_report(1000, 1000, rng)
        miss += not (lo <= 0.5 <= hi)
        a, b = sub.honest_interval(rep, 1000, 1000)
        ok += a <= 0.5 <= b
    assert miss >= 15 and ok == 20, (miss, ok)
    assert abs(sub.fresh_accuracy(1000, rng) - 0.5) < 0.06
