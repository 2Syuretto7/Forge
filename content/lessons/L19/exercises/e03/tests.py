import sub


def test_items():
    assert sub.items_needed(0.5, 0.05) == 385
    assert sub.items_needed(0.5, 0.025) == 4 * 385 - 3
    assert sub.items_needed(0.9, 0.05) < sub.items_needed(0.5, 0.05)


def test_detectable():
    assert abs(sub.detectable_difference(0.5, 500) - 1.96 * (0.5 / 500) ** 0.5) < 1e-12
    assert sub.detectable_difference(0.7, 300) > 0.07
