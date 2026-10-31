import numpy as np
import sub

P = dict(E=1.69, A=406.4, B=410.7, alpha=0.34, beta=0.28)


def test_one_epoch_is_the_data():
    assert sub.effective_tokens(1e9, 1) == 1e9


def test_few_epochs_nearly_fresh_many_epochs_saturate():
    assert sub.effective_tokens(1e9, 4) / 4e9 > 0.9
    assert sub.effective_tokens(1e9, 30) < 1e9 * 16.4 and sub.effective_tokens(1e9, 1000) / (1e9 * 16.4) < 1 + 1e-12
    assert abs(sub.effective_tokens(1e9, 1e6) / (1e9 * 16.4) - 1) < 1e-6


def test_repeats_help_less_than_fresh_data():
    fresh = sub.law(1e9, 4e10, **P)
    repeated = sub.loss_with_repeats(1e9, 1e10, 4, **P)
    once = sub.loss_with_repeats(1e9, 1e10, 1, **P)
    assert fresh < repeated < once
