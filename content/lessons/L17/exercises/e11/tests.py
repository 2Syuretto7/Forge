import numpy as np
import sub

ref = np.array([0.12, 0.18, 0.2, 0.15, 0.15, 0.1, 0.06, 0.04])
proxy = np.array([0.8, 0.9, 0.4, 0.3, -0.5, -0.2, 1.6, -1.0])
truth = np.array([1.0, 0.8, 0.4, -0.5, -0.6, -0.3, -0.8, -1.0])


def test_overoptimization():
    rows = sub.tradeoff(ref, proxy, truth, [10, 1, 0.3, 0.1, 0.02])
    kls, prox, tru = zip(*rows)
    assert all(a < b for a, b in zip(kls, kls[1:])) and all(a < b for a, b in zip(prox, prox[1:]))
    best = int(np.argmax(tru))
    assert 0 < best < 4 and tru[-1] < tru[best] - 0.5
