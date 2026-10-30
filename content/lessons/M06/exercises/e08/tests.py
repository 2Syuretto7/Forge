import math
import random
import sub


def test_small_scores():
    z = [0.5, -1.0, 2.0]
    assert abs(sub.logsumexp(z) - math.log(sum(math.exp(v) for v in z))) < 1e-14
    ls = sub.log_softmax(z)
    assert abs(sum(math.exp(v) for v in ls) - 1) < 1e-14


def test_huge_scores():
    assert abs(sub.logsumexp([1000.0, 1000.0]) - (1000 + math.log(2))) < 1e-12
    assert abs(sub.nll([1000.0, 0.0], 1) - 1000) < 1e-9


def test_bounds():
    rnd = random.Random(0)
    for _ in range(300):
        z = [rnd.uniform(-100, 100) for _ in range(rnd.randint(1, 20))]
        lse = sub.logsumexp(z)
        assert max(z) - 1e-12 <= lse <= max(z) + math.log(len(z)) + 1e-12


def test_uniform_scores():
    assert abs(sub.nll([0.0] * 10, 3) - math.log(10)) < 1e-14
