import numpy as np
import sub


def test_exp_of_uniform():
    u = np.random.default_rng(13).random(20000)
    est, se, c = sub.control_variate(np.exp(u), u, 0.5)
    p_est, p_se = sub.plain(np.exp(u))
    assert abs(est - (np.e - 1)) < 4 * se and abs(p_est - (np.e - 1)) < 4 * p_se
    assert se < p_se / 6
    assert abs(c + 1.69) < 0.02


def test_useless_control_changes_little():
    rng = np.random.default_rng(14)
    x, g = rng.random(20000), rng.random(20000)
    est, se, c = sub.control_variate(x, g, 0.5)
    assert abs(se / sub.plain(x)[1] - 1) < 0.01 and abs(c) < 0.05
