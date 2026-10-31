import numpy as np
import sub


def test_counts_and_rank():
    assert sub.lora_params(4096, 4096, 8) == 65536
    assert abs(sub.fraction(4096, 4096, 8) - 1 / 256) < 1e-15
    rng = np.random.default_rng(0)
    W0 = rng.standard_normal((30, 20))
    B, A = rng.standard_normal((30, 3)), rng.standard_normal((3, 20))
    assert sub.rank_of(sub.merged(W0, B, A) - W0) == 3
    assert sub.rank_of(W0) == 20
