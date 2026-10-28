import numpy as np
import sub

Xva, yva = sub.make_digits(1000, 2)
Xte, yte = sub.make_digits(1000, 1)
KINDS = ["sgd", "momentum", "adam", "adamw"]
_cache = {}


def _val(recipe):
    key = repr(sorted(recipe.items()))
    if key not in _cache:
        _cache[key] = sub.evaluate(sub.run(recipe, 0), Xva, yva)
    return _cache[key]


def _check_recipe(r):
    assert r["optimizer"] in KINDS, r
    assert 0 < r["steps"] <= 800 and 0 < r["batch"] <= 100, r
    assert r.get("schedule", "constant") in ("constant", "cosine"), r


def test_recipe_is_valid():
    _check_recipe(sub.RECIPE)


def test_bakeoff_covers_four_optimizers():
    assert sorted(sub.BAKEOFF) == sorted(KINDS)
    for k, entry in sub.BAKEOFF.items():
        _check_recipe(entry["recipe"])
        assert entry["recipe"]["optimizer"] == k


def test_bakeoff_reproducible():
    for k, entry in sub.BAKEOFF.items():
        got = _val(entry["recipe"])
        assert abs(got - entry["val_acc"]) <= 0.002, (k, got, entry["val_acc"])


def test_recipe_best_on_validation():
    best = max(entry["val_acc"] for entry in sub.BAKEOFF.values())
    assert _val(sub.RECIPE) >= best - 0.005


def test_recipe_test_accuracy():
    accs = [sub.evaluate(sub.run(sub.RECIPE, seed), Xte, yte) for seed in (0, 1)]
    assert np.mean(accs) >= 0.92, accs


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "validation" in text
    for k in KINDS:
        assert k in text, k
