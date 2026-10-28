import sub


def test_zero_figure_one():
    def total(z):
        return sum(sub.model_state_bytes(7.5e9, z, 64).values()) / 1e9
    assert abs(total(0) - 120) < 1e-9
    assert abs(total(1) - 31.40625) < 1e-9
    assert abs(total(2) - 16.640625) < 1e-9
    assert abs(total(3) - 1.875) < 1e-9


def test_activations():
    full = sub.activation_bytes(2048, 1, 12288, 96, 96)
    assert full == 96 * 2048 * 12288 * (34 + 80)
    assert sub.activation_bytes(2048, 1, 12288, 96, 96, tp=8, flash=True) == 96 * 2048 * 12288 * 34 / 8
    ck = sub.activation_bytes(2048, 1, 12288, 96, 96, checkpoint=True)
    assert ck == 96 * 2 * 2048 * 12288 + 2048 * 12288 * 114
    assert ck < full / 30
