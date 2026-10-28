import numpy as np
import sub

rng = np.random.default_rng(2)


def test_matches_unsharded_adam():
    n, P = 10, 3
    w = rng.normal(size=n)
    m, v = np.zeros(n), np.zeros(n)
    w_ref = w.copy()
    parts = np.array_split(np.arange(n), P)
    states = [(np.zeros(len(p)), np.zeros(len(p))) for p in parts]
    for t in range(1, 6):
        grads = [rng.normal(size=n) for _ in range(P)]
        w_ref, m, v = sub.adam_update(w_ref, sum(grads) / P, m, v, t, 0.01)
        w, states = sub.zero1_step(w, grads, states, t, 0.01)
        assert np.allclose(w, w_ref)
    assert sum(len(s[0]) for s in states) == n
