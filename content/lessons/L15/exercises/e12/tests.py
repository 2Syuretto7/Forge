import numpy as np
import sub


def test_tuned_sweep_finds_the_right_rates():
    losses, rates = sub.tuned_losses(sub.SIZES, sub.LRS)
    best = 3e-3 * (sub.SIZES / 1e6) ** -0.5
    assert np.all(np.abs(np.log2(rates / best)) <= 1)
    assert np.all(losses <= np.array([sub.sweep_loss(N, best[i]) for i, N in enumerate(sub.SIZES)]) + 0.02)


def test_fixed_rate_underestimates_the_exponent():
    tuned, rates = sub.tuned_losses(sub.SIZES, sub.LRS)
    fixed = sub.fixed_lr_losses(sub.SIZES, rates[0])
    a_tuned = sub.fitted_exponent(sub.SIZES, tuned, 1.7)
    a_fixed = sub.fitted_exponent(sub.SIZES, fixed, 1.7)
    assert abs(a_tuned - 0.25) < 0.03
    assert a_fixed < a_tuned - 0.05
    assert np.all(fixed >= tuned - 1e-12)
