import unittest
import numpy as np
import torch
import sub


def test_cached_generation_matches():
    assert sub.cached == sub.reference


def test_batched_decode_with_different_lengths():
    model, ctx = sub.model, sub.CFG["ctx"]
    prompts = [sub.val_data[i:i + n].tolist() for i, n in [(0, 5), (100, 17), (300, 11)]]
    cache = sub.KVCache(model, 4, ctx)
    toks = {s: [int(sub.prefill(model, cache, s, p).argmax())] for s, p in zip([2, 0, 3], prompts)}
    assert cache.lengths.tolist() == [17, 0, 5, 11]
    for _ in range(9):
        slots = [3, 2, 0]
        nxt = sub.decode_step(model, cache, slots, [toks[s][-1] for s in slots]).argmax(-1).tolist()
        for s, t in zip(slots, nxt):
            toks[s].append(t)
    assert cache.lengths.tolist() == [26, 0, 14, 20]
    for s, p in zip([2, 0, 3], prompts):
        assert toks[s] == sub.generate_reference(model, p, 10), s


def test_server_records():
    recs = sub.records
    assert [r["id"] for r in recs] == [r["id"] for r in sub.requests]
    for rec, req in zip(recs, sub.requests):
        assert len(rec["tokens"]) == req["max_new"] == len(rec["times"])
        assert rec["times"][0] >= req["arrival"] and all(np.diff(rec["times"]) >= 0)
    assert sub.served_match >= 0.95, sub.served_match


def test_targets():
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert sub.speedup >= sub.TARGETS["speedup"], sub.speedup
    assert sub.batched["p95_itl_ms"] <= sub.TARGETS["p95_itl_ms"], sub.batched
    assert sub.batched["p95_ttft_ms"] <= sub.TARGETS["p95_ttft_ms"], sub.batched


def test_int8():
    W = torch.randn(8, 32) * torch.logspace(-2, 1, 8)[:, None]
    q, scale = sub.quantize_int8(W)
    assert q.dtype == torch.int8 and scale.shape == (8,)
    assert (q.abs().amax(dim=1) == 127).all()
    assert ((q.float() * scale[:, None] - W).abs() <= scale[:, None] / 2 + 1e-6).all()
    lin = torch.nn.Linear(32, 8)
    x = torch.randn(4, 32)
    assert torch.allclose(sub.Int8Linear(lin)(x), lin(x), atol=0.05)
    assert sub.bytes_int8 < 0.27 * sub.bytes_fp32
    assert sub.int8_val - sub.base_val < 0.02 and sub.int8_agreement >= 0.8, (sub.int8_val, sub.int8_agreement)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "throughput" in text and "latency" in text and "int8" in text
