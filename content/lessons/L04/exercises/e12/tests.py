import numpy as np
import sub

rng = np.random.default_rng(12)


def test_grad_correct_ops_pass():
    A, B = rng.normal(size=(4, 3)), rng.normal(size=(3, 2))
    G = sub.Tensor(rng.normal(size=(4, 2)))
    ins = [sub.Tensor(A), sub.Tensor(B)]
    errs = sub.gradcheck(lambda t: ((t[0] @ t[1]).tanh() * G).sum(), ins)
    assert len(errs) == 2 and max(errs) < 1e-7, errs


def test_grad_broadcast_add_passes():
    G = sub.Tensor(rng.normal(size=(8, 4)))
    ins = [sub.Tensor(rng.normal(size=(8, 4))), sub.Tensor(rng.normal(size=4))]
    errs = sub.gradcheck(lambda t: ((t[0] + t[1]) * G).sum(), ins)
    assert max(errs) < 1e-7, errs


def test_buggy_add_flagged_on_bias_only():
    G = sub.Tensor(rng.normal(size=(32, 4)))
    ins = [sub.Tensor(rng.normal(size=(32, 4))), sub.Tensor(rng.normal(size=4))]
    errs = sub.gradcheck(lambda t: (sub.buggy_bias_add(t[0], t[1]) * G).sum(), ins)
    assert errs[0] < 1e-7, errs
    assert errs[1] > 0.5, errs


def test_inputs_restored():
    A = rng.normal(size=(3, 3))
    t = sub.Tensor(A.copy())
    sub.gradcheck(lambda ts: (ts[0] * ts[0]).sum(), [t])
    assert np.array_equal(t.data, A)
