import numpy as np
import sub

rng = np.random.default_rng(1)
F = rng.normal(size=(12, 8))
F /= np.linalg.norm(F, axis=1, keepdims=True)
X = sub.make_activations(F, 3000, 0.05, seed=2)


def test_recovers_most_features():
    P = sub.train_sae(X, 24, 0.1)
    assert sub.recovered(F, P[2]) >= 9
    assert np.allclose(np.linalg.norm(P[2], axis=1), 1)


def test_sparsity_is_needed():
    dense = sub.train_sae(X, 24, 0.01)
    assert sub.recovered(F, dense[2]) <= 5
