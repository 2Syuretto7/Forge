import sub


def test_values():
    assert sub.storage(5000, 768, 16) == 92304
    assert sub.matvec_cost(5000, 768) == 7_680_000
    assert sub.matvec_cost(5000, 768, 16) == 2 * 16 * 5768 + 16
    assert sub.gram_flops(5000, 768) == 5000 * 768 * 768


def test_break_even():
    k = sub.break_even_rank(5000, 768)
    assert sub.storage(5000, 768, k) < 5000 * 768 <= sub.storage(5000, 768, k + 1)
