import numpy as np
import sub


def test_policy_is_a_reward_model():
    rng = np.random.default_rng(0)
    for beta in (0.1, 1.0):
        ref = rng.standard_normal(6)
        ref = ref - np.log(np.sum(np.exp(ref)))
        r = rng.standard_normal(6)
        lp = sub.kl_optimal(ref, r, beta)
        assert abs(np.sum(np.exp(lp)) - 1) < 1e-12
        assert sub.same_up_to_constant(sub.implied_reward(lp, ref, beta), r)
    assert not sub.same_up_to_constant([0.0, 1.0], [0.0, 0.0])
