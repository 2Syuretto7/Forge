import numpy as np
import sub

rng = np.random.default_rng(0)
TRAIN, VALID, FRESH = sub.sample_target(300, rng), sub.sample_target(300, rng), sub.sample_target(2000, rng)


def test_diffusion_model():
    h = sub.fit(TRAIN, VALID)
    assert h > 0
    gen = sub.sample(TRAIN, h, 600)
    assert gen.shape == (600, 2)
    assert sub.sliced_w1(gen, FRESH) < 1.25 * sub.sliced_w1(TRAIN, FRESH)
    assert sub.sliced_w1(np.random.default_rng(1).standard_normal((600, 2)), FRESH) > 0.5
    assert sub.nn_distance(gen, TRAIN) > 0.7 * sub.nn_distance(FRESH[:600], TRAIN)


def test_report():
    text = sub.REPORT.lower()
    assert len(sub.REPORT.split()) >= 120
    for w in ("bandwidth", "score matching", "memoriz", "reverse"):
        assert w in text, w
