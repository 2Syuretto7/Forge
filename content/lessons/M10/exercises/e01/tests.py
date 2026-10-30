import random
import sub


def test_example():
    A = [[2, -1], [1, 1]]
    assert sub.matvec_rows(A, [3, 2]) == [4, 5]
    assert sub.matvec_cols(A, [3, 2]) == [4, 5]


def test_shape_error():
    for f in (sub.matvec_rows, sub.matvec_cols):
        try:
            f([[1, 2, 3]], [1, 2])
        except ValueError:
            continue
        raise AssertionError("expected ValueError")


def test_invariant_two_ways_and_linearity():
    rnd = random.Random(0)
    for _ in range(300):
        m, n = rnd.randint(1, 6), rnd.randint(1, 6)
        A = [[rnd.uniform(-2, 2) for _ in range(n)] for _ in range(m)]
        x = [rnd.uniform(-2, 2) for _ in range(n)]
        y = [rnd.uniform(-2, 2) for _ in range(n)]
        a, b = rnd.uniform(-2, 2), rnd.uniform(-2, 2)
        r, c = sub.matvec_rows(A, x), sub.matvec_cols(A, x)
        assert all(abs(u - v) < 1e-12 for u, v in zip(r, c))
        lhs = sub.matvec_rows(A, [a * u + b * v for u, v in zip(x, y)])
        rhs = [a * u + b * v for u, v in zip(sub.matvec_rows(A, x), sub.matvec_rows(A, y))]
        assert all(abs(u - v) < 1e-9 for u, v in zip(lhs, rhs))
