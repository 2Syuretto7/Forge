import math
import numpy as np
import sub

L2, L3, L4 = math.log(2), math.log(3), math.log(4)
T40 = 4.248354255291589e-18
INF = math.inf


def run(cases):
    bad = []
    with np.errstate(over="raise", invalid="raise", divide="raise", under="ignore"):
        for name, thunk, expected, rtol, atol in cases:
            try:
                got = np.asarray(thunk(), dtype=float)
            except (FloatingPointError, OverflowError, ValueError, ZeroDivisionError) as e:
                bad.append(f"{name}: raised {type(e).__name__}")
                continue
            exp = np.asarray(expected, dtype=float)
            if got.shape != exp.shape and exp.shape != ():
                bad.append(f"{name}: shape {got.shape}")
            elif np.isinf(exp).any():
                if not np.array_equal(got, exp):
                    bad.append(f"{name}: {got} != {exp}")
            elif not np.allclose(got, exp, rtol=rtol, atol=atol):
                bad.append(f"{name}: got {got}, expected {exp}")
    assert not bad, "; ".join(bad)


LSE = [
    ("lse of 1000s", lambda: sub.logsumexp([1000.0, 1000.0]), 1000 + L2, 1e-12, 0),
    ("lse of -1000s", lambda: sub.logsumexp([-1000.0, -1000.0]), -1000 + L2, 1e-12, 0),
    ("lse with a far term", lambda: sub.logsumexp([0.0, -1e4]), 0.0, 0, 1e-300),
    ("lse of 1e308", lambda: sub.logsumexp([1e308, 1e308]), 1e308, 1e-12, 0),
    ("lse with -inf", lambda: sub.logsumexp([-INF, 0.0]), 0.0, 0, 1e-300),
    ("lse of all -inf", lambda: sub.logsumexp([-INF, -INF]), -INF, 0, 0),
    ("lse of 800 and 0", lambda: sub.logsumexp([800.0, 0.0]), 800.0, 1e-12, 0),
    ("softmax 1000 vs 0", lambda: sub.softmax([1000.0, 0.0]), [1.0, 0.0], 0, 1e-300),
    ("softmax equal 1000s", lambda: sub.softmax([1000.0, 1000.0, 1000.0]), [1 / 3] * 3, 1e-12, 0),
    ("softmax equal -1000s", lambda: sub.softmax([-1000.0, -1000.0]), [0.5, 0.5], 1e-12, 0),
    ("softmax rows sum to 1", lambda: sub.softmax(np.array([[1000.0, -1000.0, 3.0], [-5e3, -5e3, -5e3]])).sum(axis=-1), [1.0, 1.0], 1e-12, 0),
    ("log_softmax 1000 vs 0", lambda: sub.log_softmax([1000.0, 0.0]), [0.0, -1000.0], 1e-12, 1e-300),
    ("log_softmax far term", lambda: sub.log_softmax([0.0, -1e4]), [0.0, -1e4], 1e-12, 1e-300),
    ("log_softmax equal -800s", lambda: sub.log_softmax([-800.0, -800.0, -800.0]), [-L3] * 3, 1e-12, 0),
]


SIG = [
    ("sigmoid 1000", lambda: sub.sigmoid(1000.0), 1.0, 0, 0),
    ("sigmoid -1000", lambda: sub.sigmoid(-1000.0), 0.0, 0, 1e-300),
    ("sigmoid -40", lambda: sub.sigmoid(-40.0), T40, 1e-12, 0),
    ("log_sigmoid -1000", lambda: sub.log_sigmoid(-1000.0), -1000.0, 1e-12, 0),
    ("log_sigmoid 1000", lambda: sub.log_sigmoid(1000.0), 0.0, 0, 1e-300),
    ("log_sigmoid 40", lambda: sub.log_sigmoid(40.0), -T40, 1e-12, 0),
    ("log_sigmoid -40", lambda: sub.log_sigmoid(-40.0), -40.0, 1e-12, 0),
    ("softplus 1000", lambda: sub.softplus(1000.0), 1000.0, 1e-12, 0),
    ("softplus -1000", lambda: sub.softplus(-1000.0), 0.0, 0, 1e-300),
    ("softplus -40", lambda: sub.softplus(-40.0), T40, 1e-12, 0),
]


LOSS = [
    ("ce confident right", lambda: sub.cross_entropy([[1000.0, 0.0]], [0]), 0.0, 0, 1e-300),
    ("ce confident wrong", lambda: sub.cross_entropy([[1000.0, 0.0]], [1]), 1000.0, 1e-12, 0),
    ("ce uniform", lambda: sub.cross_entropy([[0.0, 0.0, 0.0, 0.0]], [2]), L4, 1e-12, 0),
    ("ce batch", lambda: sub.cross_entropy([[800.0, -800.0], [-800.0, 800.0]], [1, 1]), 800.0, 1e-12, 0),
    ("bce right 1000", lambda: sub.bce_with_logits(1000.0, 1.0), 0.0, 0, 1e-300),
    ("bce wrong 1000", lambda: sub.bce_with_logits(1000.0, 0.0), 1000.0, 1e-12, 0),
    ("bce wrong -1000", lambda: sub.bce_with_logits(-1000.0, 1.0), 1000.0, 1e-12, 0),
    ("bce right 40", lambda: sub.bce_with_logits(40.0, 1.0), T40, 1e-12, 0),
]


STATS = [
    ("mean of 1e9 data", lambda: sub.mean_var(1e9 + np.array([1.0, 2.0, 3.0, 4.0]))[0], 1e9 + 2.5, 1e-12, 0),
    ("variance of 1e9 data", lambda: sub.mean_var(1e9 + np.array([1.0, 2.0, 3.0, 4.0]))[1], 5 / 3, 1e-12, 0),
    ("variance of 1e15 data", lambda: sub.mean_var(1e15 + np.array([0.0, 1.0, 2.0]))[1], 1.0, 1e-12, 0),
    ("variance of a constant", lambda: sub.mean_var(np.full(1000, 7.1))[1], 0.0, 0, 1e-25),
    ("log1mexp tiny", lambda: sub.log1mexp(1e-20), math.log(1e-20), 1e-12, 0),
    ("log1mexp large", lambda: sub.log1mexp(50.0), -math.exp(-50.0), 1e-12, 0),
    ("sum that cancels", lambda: sub.compensated_sum([1e16, 1.0, -1e16]), 1.0, 0, 0),
    ("ten tenths", lambda: sub.compensated_sum([0.1] * 10), 1.0, 0, 0),
]


def test_logsumexp_family():
    run(LSE)


def test_sigmoid_family():
    run(SIG)


def test_losses():
    run(LOSS)


def test_statistics_and_sums():
    run(STATS)


def test_there_are_forty_cases():
    assert len(LSE) + len(SIG) + len(LOSS) + len(STATS) == 40
