import unittest
import math
import numpy as np
import torch
import sub


def test_training():
    assert sub.loss_first > 0.9 * math.log(sub.V)
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert sub.loss_repeat < 0.5 * sub.loss_first, (sub.loss_repeat, sub.loss_first)


def test_head_scores():
    T, Hh = 6, 2
    a = torch.zeros(1, Hh, T, T)
    a[0, 0, 0, 0] = 1
    for t in range(1, T):
        a[0, 0, t, t - 1] = 1
        a[0, 1, t, 0] = 1
    a[0, 1, 0, 0] = 1
    a[0, 1, 4, 0], a[0, 1, 4, 2] = 0, 1
    prev, ind = sub.head_scores([a], [(0, 3, 2)])
    assert prev.shape == (1, 2) and ind.shape == (1, 2)
    assert np.allclose(prev[0], [1.0, 0.2]) and np.allclose(ind[0], [0.0, 0.0])
    prev, ind = sub.head_scores([a], [(0, 3, 3)])
    assert np.allclose(ind[0], [0.0, 0.5])
    p, i = sub.head_scores(sub.atts, sub.info_eval)
    assert p.shape == i.shape == (2, sub.H) and np.allclose(p, sub.prev_score)


def test_circuit_found():
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert sub.prev_heads and all(l == 0 for l, _ in sub.prev_heads)
    assert sub.induction_heads and all(l == 1 for l, _ in sub.induction_heads)
    assert max(sub.induction_score[1]) > 0.5


def test_ablation():
    base = sub.ablated_loss([])
    assert abs(base - sub.loss_repeat) < 1e-4
    assert sub.single.shape == (2, sub.H)
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    uniform = math.log(sub.V)
    assert sub.loss_prev_ablated > 0.8 * uniform and sub.loss_induction_ablated > 0.8 * uniform
    rise_circuit = sub.loss_circuit_ablated - sub.loss_repeat
    rise_rest = sub.loss_complement_ablated - sub.loss_repeat
    assert rise_rest < 0.5 * rise_circuit, (rise_rest, rise_circuit)


def test_patching():
    if abs(sub.m_clean - sub.m_corrupt) > 0.05:
        assert abs(sub.patch_effect([(l, h) for l in range(2) for h in range(sub.H)]) - 1) < 1e-3
        assert abs(sub.patch_effect([])) < 1e-6
    assert sub.effects.shape == (2, sub.H)
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    top = int(np.argmax(sub.effects[1]))
    assert (1, top) in sub.induction_heads
    assert sub.circuit_effect > 0.6, sub.circuit_effect


def test_prediction():
    acc, lo, hi = sub.pairs_acc
    assert lo <= acc <= hi and 0 <= acc <= 1
    if sub.SMALL:
        raise unittest.SkipTest("checked on the full-size run")
    assert acc > 0.4 and lo > sub.control_acc[2], (sub.pairs_acc, sub.control_acc)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    for word in ["induction", "previous-token", "ablat", "patch"]:
        assert word in text, word
