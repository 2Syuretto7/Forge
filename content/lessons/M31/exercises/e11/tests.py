import numpy as np
import sub


def test_coverage():
    accs = sub.simulate(0.92, 1000, 10000, np.random.default_rng(11))
    c_h = sub.coverage(sub.hoeffding_intervals(accs, 1000), 0.92)
    c_n = sub.coverage(sub.clt_intervals(accs, 1000), 0.92)
    assert c_h > 0.999, c_h
    assert 0.935 < c_n < 0.965, c_n
