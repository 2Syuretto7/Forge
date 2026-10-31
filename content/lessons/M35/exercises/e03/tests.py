import numpy as np
import sub


def test_bias_and_smearing():
    rng = np.random.default_rng(0)
    x = np.repeat(np.logspace(0, 2, 10), 400)
    y = 2.0 * x**-0.5 * np.exp(0.4 * rng.standard_normal(x.size))
    slope, intercept = np.polyfit(np.log(x), np.log(y), 1)
    A, alpha = np.exp(intercept), -slope
    x0 = 10.0
    true_mean = 2.0 * x0**-0.5 * sub.lognormal_mean_factor(0.4)
    naive = sub.naive_mean_prediction(A, alpha, x0)
    smeared = naive * sub.smearing_factor(sub.log_residuals(x, y, A, alpha))
    assert 0.9 < naive / true_mean < 0.95
    assert abs(smeared / true_mean - 1) < 0.02
    assert abs(sub.lognormal_mean_factor(0.4) - 1.0833) < 1e-4
