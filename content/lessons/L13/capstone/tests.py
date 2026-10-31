import unittest
import torch
import sub


def test_format_info():
    assert sub.format_info(torch.float16) == {"bits": 16, "eps": 2 ** -10, "max": 65504.0, "tiny": 2 ** -14}
    bf = sub.format_info(torch.bfloat16)
    assert bf["bits"] == 16 and bf["eps"] == 2 ** -7 and bf["max"] > 3e38 and bf["tiny"] == 2 ** -126


def test_losses_match():
    assert len(sub.amp_losses) == len(sub.fp32_losses) == sub.CFG["steps"]
    assert abs(sub.amp_final - sub.fp32_final) < 0.03 * sub.fp32_final, (sub.amp_final, sub.fp32_final)
    assert sub.amp_final < sub.amp_losses[0] - 0.5


def test_speedup_on_gpu():
    if sub.DEVICE != "cuda" or sub.SMALL:
        raise unittest.SkipTest("the speedup is measured on the full-size run on a GPU")
    assert sub.speedup >= 1.5, sub.speedup


def test_memory_on_gpu():
    if sub.DEVICE != "cuda" or sub.SMALL:
        raise unittest.SkipTest("peak memory is measured on the GPU")
    assert sub.amp_mem < sub.fp32_mem, (sub.amp_mem, sub.fp32_mem)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "scal" in text and "speedup" in text
