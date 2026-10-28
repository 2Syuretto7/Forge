import unittest
import torch
import sub

DT = torch.float16


def test_softmax_matches_torch():
    x = torch.randn(17, 200, device=sub.DEVICE, dtype=DT) * 4
    assert torch.allclose(sub.softmax(x).float(), torch.softmax(x.float(), dim=1), atol=2e-3)


def test_matmul_matches_torch():
    a = torch.randn(70, 48, device=sub.DEVICE, dtype=DT)
    b = torch.randn(48, 40, device=sub.DEVICE, dtype=DT)
    assert torch.allclose(sub.matmul(a, b).float(), a.float() @ b.float(), atol=5e-2, rtol=1e-2)


def test_layernorm_matches_torch():
    x = torch.randn(9, 100, device=sub.DEVICE, dtype=DT) * 3 + 2
    w = torch.randn(100, device=sub.DEVICE, dtype=DT)
    b = torch.randn(100, device=sub.DEVICE, dtype=DT)
    ref = torch.nn.functional.layer_norm(x.float(), (100,), w.float(), b.float())
    assert torch.allclose(sub.layernorm(x, w, b).float(), ref, atol=2e-2)


def test_flash_matches_reference():
    assert sub.flash_error < 1e-2, sub.flash_error
    q, k, v = (torch.randn(1, 40, 16, device=sub.DEVICE, dtype=DT) for _ in range(3))
    ref = sub.naive_attention(q.float(), k.float(), v.float())
    assert (sub.flash_attention(q, k, v, 16, 16).float() - ref).abs().max().item() < 1e-2


def test_flash_faster_than_naive():
    if sub.timing is None:
        raise unittest.SkipTest("timed only on a GPU with the full-size run")
    assert sub.timing["flash_ms"] < sub.timing["naive_ms"], sub.timing
