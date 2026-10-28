import numpy as np
import sub

rng = np.random.default_rng(2)


def test_train_mode_uses_batch_stats():
    bn = sub.BatchNorm(3)
    x = rng.normal(size=(8, 3)) * 2 + 5
    y = bn.forward(x)
    assert np.allclose(y.mean(axis=0), 0, atol=1e-10) and np.allclose(y.std(axis=0), 1, atol=1e-4)
    assert np.allclose(bn.running_mean, 0.1 * x.mean(axis=0))
    assert np.allclose(bn.running_var, 0.9 + 0.1 * x.var(axis=0) * 8 / 7)


def test_running_stats_converge():
    bn = sub.BatchNorm(2)
    for _ in range(300):
        bn.forward(rng.normal(size=(32, 2)) * np.array([1.0, 3.0]) + np.array([-2.0, 4.0]))
    assert np.allclose(bn.running_mean, [-2, 4], atol=0.15)
    assert np.allclose(bn.running_var, [1, 9], rtol=0.15)


def test_eval_mode():
    bn = sub.BatchNorm(2)
    bn.running_mean = np.array([1.0, -1.0])
    bn.running_var = np.array([4.0, 0.25])
    bn.training = False
    x = np.array([[3.0, -1.5], [1.0, 0.0]])
    y = bn.forward(x)
    assert np.allclose(y, (x - bn.running_mean) / np.sqrt(bn.running_var + 1e-5))
    assert np.allclose(bn.running_mean, [1, -1])
    assert np.allclose(bn.forward(x[:1]), y[:1])
