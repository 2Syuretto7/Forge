import sub


def test_well_conditioned_all_fine():
    A = sub.ill(10.0)
    for f in (sub.cgs, sub.mgs, sub.cgs2):
        assert sub.loss_of_orthogonality(f(A)) < 1e-13


def test_ill_conditioned():
    A = sub.ill(1e8)
    c, m, c2 = (sub.loss_of_orthogonality(f(A)) for f in (sub.cgs, sub.mgs, sub.cgs2))
    assert c > 1e-3, f"classical should lose orthogonality, got {c:.2e}"
    assert 1e-12 < m < 1e-6, f"modified should be near kappa * eps, got {m:.2e}"
    assert c2 < 1e-13, f"twice-run classical should be orthogonal, got {c2:.2e}"
