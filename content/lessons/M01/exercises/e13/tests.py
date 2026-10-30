import sub


def test_wrap():
    assert sub.wrap_int32(2 ** 31 - 1) == 2 ** 31 - 1
    assert sub.wrap_int32(2 ** 31) == -(2 ** 31)
    assert sub.wrap_int32(-(2 ** 31) - 1) == 2 ** 31 - 1
    assert sub.wrap_int32(5) == 5


def test_overflows():
    assert sub.overflows_int32(2 ** 31 - 1, 1)
    assert not sub.overflows_int32(2 ** 30, 2 ** 30 - 1)
    assert sub.overflows_int32(-(2 ** 31), -1)


def test_numpy_agrees_with_the_wrap():
    values = [2_000_000_000, 2_000_000_000, 500_000_000]
    exact = sum(values)
    assert sub.numpy_sum_int32(values) == sub.wrap_int32(exact)
    assert sub.numpy_sum_int32(values) != exact


def test_flops_of_a_model_do_not_fit():
    # 6 N D for a 7B model on 2T tokens, counted in int32, is garbage.
    exact = 6 * 7 * 10 ** 9 * 2 * 10 ** 12
    assert sub.wrap_int32(exact) != exact
