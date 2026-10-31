import unittest
import numpy as np
import sub


def test_benchmark_costs():
    assert len(sub.bench) >= 4
    for r in sub.bench:
        n = int(r["name"].split()[1])
        if r["name"].startswith("matmul"):
            assert r["flops"] == 2 * n ** 3 and r["bytes"] == 3 * n * n * sub.BYTES, r
        else:
            assert r["flops"] == n and r["bytes"] == 3 * n * sub.BYTES, r


def test_matmul_reaches_higher_throughput_than_add():
    best_mm = max(r["tflops"] for r in sub.bench if r["name"].startswith("matmul"))
    best_add = max(r["tflops"] for r in sub.bench if r["name"].startswith("add"))
    assert best_mm > 5 * best_add, (best_mm, best_add)


def test_fast_step_matches_slow_step():
    a, b = np.array(sub.slow_losses), np.array(sub.fast_losses)
    assert len(a) == len(b) >= 5
    assert np.allclose(a, b, rtol=2e-2, atol=1e-3), (a, b)


def test_fewer_kernels_per_step():
    assert sub.fast_kernels < sub.slow_kernels, (sub.fast_kernels, sub.slow_kernels)


def test_speedup_on_gpu():
    if sub.DEVICE != "cuda" or sub.SMALL:
        raise unittest.SkipTest("the speedup is measured on the full-size run on a GPU")
    assert sub.speedup >= 2.0, sub.speedup


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "profil" in text and "kernel" in text
