import sub


def test_skew():
    samples = ["To be, or not to be", "KING:\n  My lords,", "Exit.\n", "Enter  GHOST"]
    rate, first = sub.skew_report(samples)
    assert rate == 0.75 and first == (1, 7)
    assert sub.skew_report(["plain text"]) == (0.0, None)
