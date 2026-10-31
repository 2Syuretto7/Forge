import math
import numpy as np
import sub

N = 2000


def covered(run, truth):
    hits = 0
    widths = []
    for s in range(400, 500):
        est, lo, hi = run(np.random.default_rng(s))
        hits += lo <= truth <= hi
        widths.append(hi - lo)
    return hits, float(np.mean(widths))


def test_z():
    assert abs(sub.z_for(0.95) - 1.959964) < 1e-5
    est, lo, hi = sub.interval([1.0, 2.0, 3.0])
    assert est == 2.0 and abs((hi - lo) / 2 - sub.z_for(0.95) / math.sqrt(3)) < 1e-12


def test_integral_covers_pi():
    hits, w = covered(lambda r: sub.integrate(lambda x: 4 / (1 + x * x), 0.0, 1.0, N, r), math.pi)
    assert hits >= 93, hits
    hits4, w4 = covered(lambda r: sub.integrate(lambda x: 4 / (1 + x * x), 0.0, 1.0, 4 * N, r), math.pi)
    assert abs(w4 / w - 0.5) < 0.03


def test_expectation_covers():
    truth = 1 / math.sqrt(2 * math.pi)
    hits, _ = covered(lambda r: sub.expect(lambda z: np.maximum(z, 0), lambda g, n: g.standard_normal(n), N, r), truth)
    assert hits >= 93, hits


def test_rare_tail_covers():
    truth = 0.5 * math.erfc(4 / math.sqrt(2))
    hits, w = covered(lambda r: sub.tail_prob(4.0, N, r), truth)
    assert hits >= 93, hits
    assert w / truth < 0.2
