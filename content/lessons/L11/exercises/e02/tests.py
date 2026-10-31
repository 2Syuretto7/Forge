import sub


def test_flops_per_token():
    assert sub.train_flops_per_token(1e6, 4, 128, 192) == 6e6 + 12 * 4 * 128 * 192
    N = 12 * 4 * 192 ** 2
    f = sub.train_flops_per_token(N, 4, 128, 192)
    assert abs((f - 6 * N) / f - sub.attention_share(128, 192)) < 1e-12


def test_attention_share_values():
    assert abs(sub.attention_share(128, 192) - 128 / 1280) < 1e-12
    assert sub.attention_share(2048, 768) > sub.attention_share(2048, 12288)
    assert abs(sub.attention_share(6, 1) - 0.5) < 1e-12


def test_budget_and_mfu():
    assert abs(sub.tokens_for_budget(6e18, 1e9) - 1e9) < 1e-3
    assert abs(sub.mfu(1e5, 6e8, 65e12) - 6e13 / 65e12) < 1e-12
