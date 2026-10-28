import unittest
import numpy as np
import sub


def test_plan_within_budget():
    for key in ["pretrain", "sft", "rl"]:
        assert key in sub.PLAN
    assert sub.plan_flops <= sub.BUDGET, sub.plan_flops


def test_clean_crawl():
    kinds = sub.kept_kinds
    assert kinds.count("leak") == 0
    assert kinds.count("junk") <= 0.02 * sub.kinds.count("junk")
    assert kinds.count("source") >= 0.8 * sub.kinds.count("source")
    assert all(sub.FOOTER not in sub.cleaned[i] for i in sub.kept)


def test_manifest():
    assert [r["stage"] for r in sub.MANIFEST] == ["clean", "pretrain", "finetune", "rl", "serve"]
    assert sub.check_chain(sub.MANIFEST, sub.raw_digest) is None
    broken = [dict(r) for r in sub.MANIFEST]
    broken[2]["input"] = "000000000000"
    assert sub.check_chain(broken, sub.raw_digest) == 2


def test_evaluation():
    for stage in ["pretrained", "fine-tuned", "RL"]:
        r = sub.STAGES[stage]
        for task in ["UPPER", "REVERSE"]:
            assert len(r[task]) == len(sub.test_words) and set(np.unique(r[task])) <= {0.0, 1.0}
            assert len(r[task + "_sampled"]) == len(sub.test_words)
    assert sub.rl_reward("UPPER", "king", "KING\n") == 1.0 and sub.rl_reward("UPPER", "king", "KING ") == 0.0


def test_stages_improve():
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert sub.pretrain_val < 1.9, sub.pretrain_val
    ft, rl = sub.STAGES["fine-tuned"], sub.STAGES["RL"]
    assert ft["UPPER"].mean() >= 0.8, ft["UPPER"].mean()
    assert ft["val"] - sub.pretrain_val < 0.1
    assert sub.rl_gain[1] > 0, sub.rl_gain


def test_serving():
    assert sub.serving["match"] >= 0.95
    if sub.SMALL:
        raise unittest.SkipTest("latency is checked on the full-size run")
    assert sub.serving["p95_itl_ms"] <= 50, sub.serving


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 200
    for word in ["clean", "pretrain", "lora", "rl", "serv", "["]:
        assert word in text, word
