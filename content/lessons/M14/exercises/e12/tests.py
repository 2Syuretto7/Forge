import numpy as np
import sub

D = sub.make_update()


def test_params():
    assert sub.lora_params(4096, 4096, 8) == 65536
    assert sub.lora_params(4096, 4096, 8) / 4096 ** 2 < 0.004


def test_factors():
    B, A = sub.best_rank_r(D, 8)
    assert B.shape == (256, 8) and A.shape == (8, 256)
    err = np.linalg.norm(D - B @ A) / np.linalg.norm(D)
    assert np.isclose(err ** 2, 1 - sub.captured(D, 8))
    assert sub.captured(D, 8) > 0.98
