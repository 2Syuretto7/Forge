import numpy as np
import sub


def test_sketch_is_close():
    rng = np.random.default_rng(0)
    A = rng.standard_normal((5000, 30))
    b = A @ rng.standard_normal(30) + rng.standard_normal(5000)
    ratios = []
    for s in (100, 300):
        r = np.mean([sub.residual_ratio(A, b, sub.sketched_lstsq(A, b, s, rng)) for _ in range(3)])
        ratios.append(r)
        assert 1 <= r < 1.1 * sub.predicted_ratio(30, s), (s, r)
    assert ratios[1] < ratios[0]
    SA, Sb = sub.sketch(A, b, 100, rng)
    assert SA.shape == (100, 30) and Sb.shape == (100,)
