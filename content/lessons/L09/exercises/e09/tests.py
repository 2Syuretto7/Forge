import sub


def test_gpt2_small():
    assert sub.gpt_params(50257, 1024, 768, 12) == 124_439_808


def test_small_config():
    d = 128
    block = 12 * d * d + 13 * d
    assert sub.gpt_params(65, 128, d, 2) == 65 * d + 128 * d + 2 * block + 2 * d


def test_flops_and_crossover():
    assert sub.forward_flops_per_token(768, 12, 1024) == 24 * 12 * 768 ** 2 + 4 * 12 * 1024 * 768
    n = sub.attention_crossover_ctx(768)
    assert n == 4608
    assert sub.forward_flops_per_token(768, 12, n) == 2 * 24 * 12 * 768 ** 2
