import unittest
import torch
import sub


def test_encode_example():
    ids, mask = sub.encode_example("UPPER", "king")
    assert bytes(ids).decode() == "UPPER: king\n=KING\n"
    assert mask == [0] * 13 + [1] * 5


def test_masked_loss():
    torch.manual_seed(0)
    logits, y = torch.randn(2, 3, 5), torch.randint(0, 5, (2, 3))
    mask = torch.tensor([[0.0, 1, 1], [0, 0, 1]])
    per = torch.nn.functional.cross_entropy(logits.flatten(0, 1), y.flatten(), reduction="none").view(2, 3)
    assert torch.allclose(sub.masked_loss(logits, y, mask), (per[0, 1] + per[0, 2] + per[1, 2]) / 3)


def test_lora_layer():
    torch.manual_seed(0)
    lin = torch.nn.Linear(6, 4)
    lora = sub.LoRALinear(lin, 2, 4)
    x = torch.randn(3, 6)
    assert torch.allclose(lora(x), lin(x))
    with torch.no_grad():
        lora.B.normal_()
    expected = lin(x) + 2.0 * (x @ lora.A.T) @ lora.B.T
    assert torch.allclose(lora(x), expected, atol=1e-6)
    assert torch.allclose(lora.merge()(x), expected, atol=1e-5)


def test_adapters_and_merge():
    r = sub.results["lora"]
    assert r["trainable"] < (0.5 if sub.SMALL else 0.15) * sum(p.numel() for p in sub.base.parameters())
    assert sub.merge_error < 1e-4


def test_targets():
    assert set(sub.test_words).isdisjoint(sub.train_words)
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert sub.lora_accuracy >= sub.TARGETS["accuracy"], sub.results["lora"]["eval"]
    assert sub.lora_forgetting <= sub.TARGETS["forgetting"], sub.lora_forgetting


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "lora" in text and "forgetting" in text and "full fine-tuning" in text and "replay" in text
