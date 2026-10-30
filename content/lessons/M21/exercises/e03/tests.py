import sub


def test_grad_derivative():
    h = 1e-7
    for pi in (0.001, 0.05, 0.3, 0.8):
        for s, f in ((0.99, 0.01), (0.8, 0.2)):
            num = (sub.post(pi + h, s, f) - sub.post(pi - h, s, f)) / (2 * h)
            assert abs(num - sub.dpost_dprior(pi, s, f)) < 1e-6 * max(1, abs(num))


def test_values():
    assert abs(sub.post(0.001, 0.99, 0.01) - 0.0901639344) < 1e-9
    pi = sub.prior_needed(0.5, 0.99, 0.01)
    assert abs(sub.post(pi, 0.99, 0.01) - 0.5) < 1e-12 and abs(pi - 0.01) < 1e-3
