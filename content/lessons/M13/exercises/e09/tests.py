import sub


def test_exact():
    assert [sub.fib_power(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert sub.fib_power(100) == 354224848179261915075


def test_binet_until_floats_run_out():
    k = sub.first_disagreement()
    assert 65 < k < 85, k
    assert all(sub.fib_binet(n) == sub.fib_power(n) for n in range(k))
