import sub


def test_scaled_is_stable_in_d():
    small, big = sub.saturation(16, True), sub.saturation(512, True)
    assert small[0] < 0.4 and big[0] < 0.4
    assert abs(small[1] - big[1]) < 0.02


def test_unscaled_saturates():
    m512, g512 = sub.saturation(512, False)
    assert m512 > 0.9
    assert g512 < sub.saturation(512, True)[1] / 5
