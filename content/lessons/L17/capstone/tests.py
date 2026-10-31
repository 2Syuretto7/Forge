import unittest
import torch
import sub


def test_reward():
    assert sub.reward("57", 23, 34) == 1.0
    assert sub.reward("56", 23, 34) == 0.0 and sub.reward("57 ", 23, 34) == 0.0 and sub.reward("", 23, 34) == 0.0


def test_group_advantages():
    a = sub.group_advantages(torch.tensor([[1.0, 0, 0, 1], [1, 1, 1, 1]]))
    assert torch.allclose(a[0], torch.tensor([1.0, -1, -1, 1]) / (torch.tensor([1.0, 0, 0, 1]).std() * 2), atol=1e-4)
    assert torch.allclose(a[1], torch.zeros(4))


def test_rl_loss():
    torch.manual_seed(0)
    logp = -torch.rand(3, 4)
    ref = -torch.rand(3, 4)
    adv = torch.tensor([1.0, -0.5, 0.0])
    mask = torch.tensor([[1.0, 1, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0]])
    u = ref - logp
    expected = ((-adv[:, None] * logp + 0.1 * (u.exp() - 1 - u)) * mask).sum() / 6
    assert torch.allclose(sub.rl_loss(logp, ref, adv, mask, 0.1), expected)
    assert torch.allclose(sub.rl_loss(logp, logp, torch.zeros(3), mask, 0.5), torch.tensor(0.0))


def test_rl_helps():
    assert len(sub.sft_eval["sampled"]) == len(sub.test_pairs)
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    low, high = sub.runs[sub.low_beta], sub.runs[sub.high_beta]
    assert sub.gains[sub.low_beta][1] > 0.1, sub.gains
    assert low["eval"]["sampled"].mean() > high["eval"]["sampled"].mean() + 0.05
    assert low["kl"] > high["kl"], (low["kl"], high["kl"])


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "kl" in text and "accuracy" in text and "reward" in text
