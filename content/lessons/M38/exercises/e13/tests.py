import numpy as np
import sub


def test_adam_handles_bad_scaling():
    s = np.logspace(-2, 2, 50)
    r = sub.compare(s, np.ones(50))
    assert r["adam"] is not None and r["gd"] is not None
    assert r["gd"] > 5 * r["adam"], r
