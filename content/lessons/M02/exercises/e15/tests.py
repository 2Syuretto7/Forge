import sub


def test_finds_the_planted_errors():
    assert sub.bad_steps(sub.CHAIN, sub.NAMES) == [2, 5]


def test_a_correct_chain_passes():
    chain = [("*", ("+", "x", 1), ("-", "x", 1)), ("-", ("^", "x", 2), 1)]
    assert sub.bad_steps(chain, ["x"]) == []


def test_the_true_answer():
    # (a + b)^2 - (a - b)^2 = 4ab, which the chain's last step reaches by a lucky second error.
    env = {"a": 1.5, "b": -2.0}
    assert abs(sub.evaluate(sub.CHAIN[0], env) - 4 * 1.5 * -2.0) < 1e-12
