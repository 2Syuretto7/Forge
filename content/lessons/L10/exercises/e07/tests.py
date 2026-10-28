import numpy as np
import sub

X, Y = sub.make_digits(200, 0)
P = sub.init_stack(20, 64, seed=0)
STATS = {m: sub.layer_stats(P, X, Y, 20, m) for m in sub.MODES}


def test_lengths():
    for acts, grads in STATS.values():
        assert len(acts) == 20 and len(grads) == 20


def test_post_norm_keeps_unit_scale():
    assert np.allclose(STATS["post"][0], 1.0, atol=1e-3)


def test_unnormalized_residual_explodes():
    acts = STATS["res"][0]
    assert acts[-1] > 1e3 * acts[0]


def test_pre_norm_grows_slowly():
    acts = STATS["pre"][0]
    assert 3 < acts[-1] / acts[0] < 30


def test_layer_norm_without_residuals_skews_gradients():
    grads = STATS["plain_ln"][1]
    assert grads[0] > 10 * grads[-1]
    plain = STATS["plain"][1]
    assert 1 / 3 < plain[0] / plain[-1] < 3
