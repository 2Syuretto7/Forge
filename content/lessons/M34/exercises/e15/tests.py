import numpy as np
import sub


def test_shared_component():
    rng = np.random.default_rng(0)
    X = sub.anisotropic(300, 512, 1.0, rng)
    assert abs(sub.mean_pairwise_cosine(X) - sub.predicted_cosine(1.0)) < 0.03
    assert abs(sub.mean_pairwise_cosine(sub.center(X))) < 0.01
    iso = rng.standard_normal((300, 512))
    assert abs(sub.mean_pairwise_cosine(iso)) < 0.01
    assert abs(sub.predicted_cosine(2.0) - 0.8) < 1e-12
