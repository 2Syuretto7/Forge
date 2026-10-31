import numpy as np
import sub


def runs(proposal):
    return [sub.is_run(proposal, 10000, np.random.default_rng(s)) for s in range(50)]


def test_light_tailed_proposal_fails():
    r = runs("normal")
    cover = np.mean([abs(m - 2) <= 1.96 * se for m, se, _ in r])
    assert cover < 0.7, cover
    assert np.median([m for m, _, _ in r]) < 1.8


def test_heavy_tailed_proposal_works():
    r = runs("laplace2")
    cover = np.mean([abs(m - 2) <= 1.96 * se for m, se, _ in r])
    assert cover > 0.85, cover
    assert all(0.6 < e < 0.9 for *_, e in r)


def test_laplace_pieces():
    x = sub.laplace_sample(1.0, 200000, np.random.default_rng(60))
    assert abs(np.mean(x * x) - 2) < 0.05 and abs(np.mean(x)) < 0.01
    assert abs(float(sub.laplace_logpdf(0.0)) + np.log(2)) < 1e-12
