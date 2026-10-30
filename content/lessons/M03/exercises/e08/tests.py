import random
import sub

R = range(-50, 51)


def test_even_squares():
    p = lambda n: (n * n) % 2 == 0
    q = lambda n: n % 2 == 0
    assert sub.failures(p, q, R) == []
    assert sub.contrapositive_failures(p, q, R) == []


def test_converse_differs():
    p = lambda n: n > 2
    q = lambda n: n * n > 4
    assert sub.failures(p, q, R) == []
    assert sub.converse_failures(p, q, R) == [n for n in R if n < -2]


def test_invariant_contrapositive_fails_at_the_same_cases():
    rnd = random.Random(3)
    for _ in range(300):
        tp = {x: rnd.random() < 0.5 for x in R}
        tq = {x: rnd.random() < 0.5 for x in R}
        p, q = (lambda x: tp[x]), (lambda x: tq[x])
        assert sub.failures(p, q, R) == sub.contrapositive_failures(p, q, R)
