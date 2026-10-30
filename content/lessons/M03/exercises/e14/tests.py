import sub


def test_horses():
    assert sub.overlap(5) == 4
    assert not sub.step_works(1) and sub.step_works(2)
    assert sub.first_broken_step() == 1


def test_odd_numbers():
    assert all(sub.step_holds(n) for n in range(1000))
    assert not sub.base_holds()
    assert not any(sub.claim_holds(n) for n in range(1000))
