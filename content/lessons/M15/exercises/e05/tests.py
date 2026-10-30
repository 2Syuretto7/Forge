import math
import random
import sub

PAIRS = [
    (math.sin, math.cos, math.exp, math.exp),
    (lambda x: x ** 3, lambda x: 3 * x * x, math.cos, lambda x: -math.sin(x)),
    (math.tanh, lambda x: 1 - math.tanh(x) ** 2, lambda x: x * x + 1, lambda x: 2 * x),
]


def central(F, x, h=1e-5):
    return (F(x + h) - F(x - h)) / (2 * h)


def test_grad_rules_match_central_differences():
    rnd = random.Random(5)
    for f, df, g, dg in PAIRS:
        for _ in range(10):
            x = rnd.uniform(0.2, 1.5)
            for rule, F in [
                (sub.product_rule, lambda t: f(t) * g(t)),
                (sub.quotient_rule, lambda t: f(t) / g(t)),
                (sub.chain_rule, lambda t: f(g(t))),
            ]:
                exact = rule(f, df, g, dg)(x)
                assert abs(exact - central(F, x)) <= 1e-6 * max(1, abs(exact)), (rule.__name__, x)
