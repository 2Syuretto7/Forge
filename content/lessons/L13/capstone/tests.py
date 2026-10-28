import unittest
import torch
import sub


def test_attention_matches_pytorch():
    torch.manual_seed(1)
    m = sub.CausalSelfAttention(32, 4).to(sub.DEVICE)
    x = torch.randn(2, 10, 32, device=sub.DEVICE)
    with torch.no_grad():
        assert torch.allclose(m(x), sub.reference_attention(m, x), atol=1e-5)


def test_causality():
    torch.manual_seed(2)
    model = sub.GPT(sub.VOCAB, 16, 32, 2, 4).to(sub.DEVICE).eval()
    idx = torch.randint(sub.VOCAB, (1, 16), device=sub.DEVICE)
    changed = idx.clone()
    changed[0, 10:] = (changed[0, 10:] + 1) % sub.VOCAB
    with torch.no_grad():
        a, b = model(idx), model(changed)
    assert torch.allclose(a[0, :10], b[0, :10], atol=1e-6)
    assert not torch.allclose(a[0, 10:], b[0, 10:])


def test_param_formula():
    for vocab, ctx, d, layers in [(65, 128, 128, 2), (100, 64, 48, 3)]:
        m = sub.GPT(vocab, ctx, d, layers, 4)
        assert sum(p.numel() for p in m.parameters()) == sub.param_formula(vocab, ctx, d, layers)


def test_training_reduces_loss():
    first, last = sub.losses[0][1], sub.losses[-1][1]
    assert last < first - 0.5, sub.losses


def test_validation_loss_target():
    if sub.SMALL:
        raise unittest.SkipTest("the target applies to the full training run")
    assert sub.val_loss < 1.70, sub.val_loss


def test_sample():
    assert len(sub.sample_text) == len("ROMEO:\n") + 300
    assert set(sub.sample_text) <= set(sub.chars)
