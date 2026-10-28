import numpy as np
import sub

X, Y = sub.make_digits(6, 0)


def _check(mode):
    p = sub.init_stack(3, 8, seed=1)
    for k in p:
        if k[0] in "gb":
            p[k] = p[k] + 0.1 * np.arange(p[k].size)
    _, g = sub.stack_loss_and_grads(p, X, Y, 3, mode)
    assert sorted(g) == sorted(p)
    for k in ["Win", "W0", "W2", "g1", "b2", "gf", "bf", "Wout"]:
        num = np.zeros_like(p[k])
        for idx in list(np.ndindex(p[k].shape))[:12]:
            old = p[k][idx]
            p[k][idx] = old + 1e-6
            lp, _ = sub.stack_loss_and_grads(p, X, Y, 3, mode)
            p[k][idx] = old - 1e-6
            lm, _ = sub.stack_loss_and_grads(p, X, Y, 3, mode)
            p[k][idx] = old
            num[idx] = (lp - lm) / 2e-6
            assert abs(num[idx] - g[k][idx]) < 1e-6, (mode, k, idx)


def test_grad_plain():
    _check("plain")


def test_grad_plain_ln():
    _check("plain_ln")


def test_grad_res():
    _check("res")


def test_grad_pre():
    _check("pre")


def test_grad_post():
    _check("post")


def test_forward_shapes():
    p = sub.init_stack(4, 16)
    for mode in sub.MODES:
        logits, hidden, _ = sub.stack_forward(p, X, 4, mode)
        assert logits.shape == (6, 10) and hidden.shape == (6, 16)
