import numpy as np
import sub

rng = np.random.default_rng(2)
logits, ref = rng.normal(size=(6, 4)), rng.normal(size=(6, 4))
actions = rng.integers(0, 4, 6)
adv = rng.normal(size=6)


def test_advantages():
    a = sub.group_advantages([[1, 0, 0, 1], [1, 1, 1, 1]])
    assert np.allclose(a[0], [1, -1, -1, 1], atol=1e-5) and np.allclose(a[1], 0)


def test_grad_pg():
    _, g = sub.pg_loss(logits, actions, adv, ref, 0.1)
    num = np.zeros_like(logits)
    for idx in np.ndindex(logits.shape):
        E = np.zeros_like(logits); E[idx] = 1e-6
        num[idx] = (sub.pg_loss(logits + E, actions, adv, ref, 0.1)[0] - sub.pg_loss(logits - E, actions, adv, ref, 0.1)[0]) / 2e-6
    assert np.allclose(g, num, atol=1e-8)
    assert abs(sub.pg_loss(logits, actions, np.zeros(6), logits, 0.5)[0]) < 1e-12
