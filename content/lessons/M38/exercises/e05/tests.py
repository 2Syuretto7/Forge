import numpy as np
import sub


def test_no_optimum():
    ref = np.log(np.ones(3) / 3)
    N = np.zeros((3, 3))
    N[0, 1] = 50
    zs = [sub.train_dpo(ref, N, 0.5, s) for s in (1000, 5000, 20000)]
    losses = [sub.loss_at(z, ref, N, 0.5) for z in zs]
    gaps = [z[0] - z[1] for z in zs]
    assert losses[0] > losses[1] > losses[2] > 0
    assert gaps[0] < gaps[1] < gaps[2]
    assert sub.prob_gap(zs[2]) > sub.prob_gap(zs[0])
