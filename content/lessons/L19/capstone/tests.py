import math
import torch
import sub


def test_schedule():
    cfg = dict(lr=1e-3, warmup=100, steps=1000)
    assert sub.lr_at(1, cfg) == 1e-5 and sub.lr_at(100, cfg) == 1e-3
    assert abs(sub.lr_at(1000, cfg) - 1e-4) < 1e-15 and abs(sub.lr_at(550, cfg) - 5.5e-4) < 1e-15


def test_exact_resume():
    assert sub.resume_exact is True


def test_checkpoints():
    files = sorted(sub.CKPT_DIR.glob("step-*.pt"))
    assert files and not list(sub.CKPT_DIR.glob("*.tmp"))
    state = torch.load(files[-1], map_location="cpu", weights_only=False)
    for key in ["model", "opt", "scaler", "step", "pos", "log", "cfg", "rng_cpu"]:
        assert key in state, key


def test_spike_detected_and_rolled_back():
    cfg = sub.CFG
    assert 1 <= len(sub.spikes) <= 2, sub.spikes
    s = sub.spikes[0]
    assert cfg["bad_start"] <= s["flagged_pos"] <= cfg["bad_start"] + 2, s
    assert s["restored_step"] < cfg["bad_start"] and s["restored_step"] % cfg["ckpt_every"] == 0
    assert s["skipped"][1] >= cfg["bad_start"] + cfg["bad_len"] - 1


def test_log():
    steps = [e for e in sub.run["log"] if "loss" in e]
    assert [e["step"] for e in steps] == list(range(1, sub.CFG["steps"] + 1))
    assert all(math.isfinite(e["loss"]) and e["grad_norm"] >= 0 and e["lr"] > 0 and e["tokens_per_s"] > 0 for e in steps)
    assert all(e["pos"] not in sub.BAD for e in steps)


def test_evaluation_and_recovery():
    assert sub.final_low <= sub.final_val <= sub.final_high and len(sub.final_per) == sub.CFG["eval_windows"]
    first = sub.evals[0]["val"]
    assert sub.final_val < first
    if not sub.SMALL:
        assert sub.final_val < 1.70 and sub.final_val < sub.pre_spike_val, (sub.final_val, sub.pre_spike_val)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "spike" in text and "validation" in text and "rolled back" in text
