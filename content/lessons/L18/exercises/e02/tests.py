import numpy as np
import sub

rng = np.random.default_rng(0)


def test_allreduce_sums():
    for P in [1, 2, 3, 5]:
        xs = [rng.normal(size=11) for _ in range(P)]
        out, _ = sub.ring_allreduce(xs)
        assert len(out) == P and all(np.allclose(o, sum(xs)) for o in out)


def test_traffic():
    for P in [2, 4, 8]:
        _, sent = sub.ring_allreduce([np.ones(64) for _ in range(P)])
        assert sent == 2 * (P - 1) * 64 // P


def test_inputs_unchanged():
    xs = [np.ones(4), 2 * np.ones(4)]
    sub.ring_allreduce(xs)
    assert np.all(xs[0] == 1) and np.all(xs[1] == 2)
