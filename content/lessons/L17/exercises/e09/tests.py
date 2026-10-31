import numpy as np
import sub


def test_extract_and_reward():
    assert sub.extract_answer("3 + 4 is 7. Answer: 7") == 7
    assert sub.extract_answer("no digits") is None and sub.extract_answer("Answer: -12") == -12
    assert sub.reward("work... Answer: 7", 7) == 1.0
    assert sub.reward("it is 7", 7) == 0.5 and sub.reward("it is 7", 7, want_format=False) == 1.0
    assert sub.reward("Answer: 8", 7) == 0.0


def test_group_advantages():
    a = sub.group_advantages([1, 0, 0, 1])
    assert np.allclose(a, [1, -1, -1, 1], atol=1e-5)
    assert np.allclose(sub.group_advantages([1, 1, 1]), 0)
