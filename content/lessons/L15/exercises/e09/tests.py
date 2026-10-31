import numpy as np
import sub

BAD = set(range(150, 155))


def test_recovery_matches_a_clean_run():
    clean, f_clean = sub.run(200, set())
    recovered, flagged = sub.run(200, BAD)
    broken, _ = sub.run(200, BAD, recover=False)
    assert f_clean == [] and flagged == [150]
    assert np.abs(recovered - sub.TRUE_W).max() < 0.01
    assert np.abs(broken - sub.TRUE_W).max() > 0.2
