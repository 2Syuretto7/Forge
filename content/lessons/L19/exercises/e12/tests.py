import sub


def test_audit():
    good = [(s, sub.expected_lr(s, 1e-3, 200, 6000)) for s in range(1, 6001, 7)]
    assert sub.audit_lr(good, 1e-3, 200, 6000) is None
    bad = [(s, sub.expected_lr(s if s <= 3000 else s - 3000, 1e-3, 200, 6000)) for s in range(1, 6001)]
    assert sub.audit_lr(bad, 1e-3, 200, 6000) == 3001
    assert sub.expected_lr(200, 1e-3, 200, 6000) == 1e-3
