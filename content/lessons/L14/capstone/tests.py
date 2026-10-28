import unittest
import torch
import sub


def test_tokenizer_roundtrip():
    for s in ["ROMEO:\nBut, soft!", "  leading and trailing  \n", "naïve café 東京", sub.val_text[:500]]:
        assert sub.tok.decode(sub.tok.encode(s)) == s


def test_tokenizer_compresses():
    assert len(sub.tok.vocab) == sub.VOCAB_SIZE
    assert sub.chars_per_token > (1.3 if sub.SMALL else 1.7), sub.chars_per_token


def test_filters():
    logits = torch.tensor([3.0, 2.0, 1.0, 0.0, -1.0], device=sub.DEVICE)
    k = sub.filter_logits(logits, top_k=2)
    assert torch.isfinite(k).sum() == 2 and torch.isfinite(k[:2]).all()
    p = sub.filter_logits(logits, top_p=0.9)
    probs = torch.softmax(logits, 0)
    assert torch.isfinite(p).sum() == 3 and probs[:2].sum() < 0.9 <= probs[:3].sum()
    assert torch.equal(sub.filter_logits(logits), logits)


def test_training_reduces_validation_loss():
    first, last = sub.history[0][2], sub.history[-1][2]
    assert last < first - 0.5, sub.history


def test_bits_per_character_target():
    if sub.SMALL:
        raise unittest.SkipTest("the target applies to the full training run")
    assert sub.val_bits_per_char < 2.3, sub.val_bits_per_char


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "bits per character" in text and "temperature" in text
