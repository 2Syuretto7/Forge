import math
import sub

T = sub.truths()
NAMES = ["mlp_flops", "mlp_params", "embedding_bytes", "adam_gb", "train_flops", "gpu_hours", "run_cost",
         "imagenet_bytes", "steps_per_epoch", "attention_entries", "corpus_words", "corpus_chars"]


def test_truths_of_the_model_quantities():
    assert T["mlp_flops"] == 85590016
    assert T["mlp_params"] == 669706
    assert T["embedding_bytes"] == 153600000
    assert math.isclose(T["adam_gb"], 20.8, rel_tol=1e-12)
    assert math.isclose(T["attention_entries"], 402653184, rel_tol=0)


def test_truths_of_the_run():
    assert math.isclose(T["train_flops"], 1.875e18, rel_tol=1e-12)
    assert math.isclose(T["gpu_hours"], 1.875e18 / 4e13 / 3600, rel_tol=1e-12)
    assert math.isclose(T["run_cost"], 2 * 1.875e18 / 4e13 / 3600, rel_tol=1e-12)


def test_truths_of_the_data():
    assert T["imagenet_bytes"] == 1281167 * 150528
    assert T["steps_per_epoch"] == 5005
    assert T["corpus_words"] == len(sub.CORPUS.split())
    assert T["corpus_chars"] == len(sub.CORPUS)
    assert 3000 * 8 <= T["corpus_words"] <= 3000 * 20


def test_estimates_are_honest_intervals():
    assert sorted(sub.ESTIMATES) == sorted(NAMES), "give an interval for each of the twelve names"
    for name, (lo, hi) in sub.ESTIMATES.items():
        assert 0 < lo < hi, f"{name}: need 0 < lo < hi"
        assert hi / lo <= 30, f"{name}: the interval spans a factor of {hi / lo:.0f}; at most 30"


def test_score():
    assert sub.score({"a": (1, 9)}, {"a": 9}) == 1
    assert sub.score({"a": (1, 9)}, {"a": 9.1}) == 0
    s = sub.score(sub.ESTIMATES, T)
    assert s >= 10, f"{s} of 12 within a factor of 3; the capstone needs at least 10"
