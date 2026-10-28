import numpy as np
import sub

p = np.array([0.5, 0.3, 0.15, 0.05])
q = np.array([0.25, 0.25, 0.25, 0.25])
rng = np.random.default_rng(7)
ys = rng.choice(4, size=200000, p=p)


def test_unbiased_and_nonnegative():
    k1, k3 = sub.kl_estimators(np.log(p[ys]), np.log(q[ys]))
    true = sub.exact_kl(p, q)
    assert abs(k1.mean() - true) < 0.01 and abs(k3.mean() - true) < 0.01
    assert np.all(k3 >= 0) and np.any(k1 < 0)
    assert k3.var() < k1.var()
