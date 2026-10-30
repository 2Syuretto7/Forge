import sub


def test_synthetic():
    assert abs(sub.observed_rate([0.5 ** k for k in range(40)]) - 0.5) < 1e-12
    assert sub.predicted_steps(0.5, 1e-3, 1.0) == 10


def test_damping_bounds_rate():
    src, dst = sub.make_graph(5000, seed=1)
    rates = []
    for d in (0.5, 0.85, 0.95):
        _, res = sub.pagerank_sparse(src, dst, 5000, d=d, tol=1e-12)
        rate = sub.observed_rate(res)
        assert rate <= d + 0.01, (d, rate)
        rates.append(rate)
    assert rates[0] < rates[1] < rates[2]
