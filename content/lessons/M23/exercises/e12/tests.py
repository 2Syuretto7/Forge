import sub

ALPHAS = [0.0, 0.01, 0.03, 0.1, 0.3, 0.5]


def test_best_alpha_falls_with_data():
    a = sub.alpha_curve([300, 1000, 10000], ALPHAS)
    assert a[0] >= 0.3 and a[2] <= 0.1, a
    assert a[0] >= a[1] >= a[2], a


def test_best_alpha_picks_the_maximum():
    X, V = sub.make_embeddings(600, 5), sub.make_embeddings(1000, 6)
    a = sub.best_alpha(X, V, ALPHAS)
    assert all(sub.heldout_loglik(X, V, a) >= sub.heldout_loglik(X, V, b) for b in ALPHAS)
