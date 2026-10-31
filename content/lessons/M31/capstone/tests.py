import math
import numpy as np
import sub


def test_intervals():
    c = sub.make_eval()
    acc, lo, hi = sub.hoeffding_interval(c)
    assert abs((hi - lo) / 2 - math.sqrt(math.log(40) / 4000)) < 1e-12 and lo < acc < hi
    acc2, blo, bhi = sub.bootstrap_interval(c)
    assert acc2 == acc and (bhi - blo) < (hi - lo) and blo < acc < bhi


def test_reuse():
    r = sub.reuse_experiment()
    assert 0.03 < r["inflation"] < sub.union_epsilon(1000, 1000), r
    assert abs(r["fresh"] - 0.5) < 0.05


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    assert "hoeffding" in text and "bootstrap" in text and "union bound" in text
