import numpy as np
import sub


def test_engine_matches_pytorch():
    e = np.array(sub.engine_losses)
    t = np.array(sub.torch_losses)
    assert len(e) == len(t) >= 20
    assert np.max(np.abs(e - t)) < 1e-6, np.max(np.abs(e - t))


def test_engine_learns():
    assert sub.engine_losses[-1] < 0.7 * sub.engine_losses[0]


def test_grad_fn_walk():
    ops = set(sub.grad_fn_names)
    assert any("Addmm" in o or "Mm" in o for o in ops), ops
    assert any("Relu" in o for o in ops), ops
    assert any("NllLoss" in o or "LogSoftmax" in o for o in ops), ops
    assert "AccumulateGrad" in ops


def test_custom_function():
    assert sub.custom_gradcheck_ok is True
    assert sub.custom_matches_autograd < 1e-12
