import numpy as np
import sub

KS = [5, 10, 20, 40]


def test_near_optimal_with_one_power_iteration():
    rng = np.random.default_rng(0)
    A = sub.make_matrix(3000, 300, 1.5, rng)
    s = 1 / np.arange(1, 301) ** 1.5
    got = sub.relative_errors(A, KS, 10, 1, rng)
    opt = sub.optimal_errors(s, KS)
    assert all(g / o < 1.02 for g, o in zip(got, opt)), (got, opt)


def test_power_iterations_on_slow_decay():
    rng = np.random.default_rng(1)
    A = sub.make_matrix(3000, 300, 0.5, rng)
    opt = sub.optimal_errors(1 / np.sqrt(np.arange(1, 301)), [20])[0]
    q0 = sub.relative_errors(A, [20], 5, 0, rng)[0]
    q2 = sub.relative_errors(A, [20], 5, 2, rng)[0]
    assert q2 < q0 and q2 / opt < 1.02 < q0 / opt, (q0 / opt, q2 / opt)
    assert sub.matvecs(20, 5, 2) == 150
