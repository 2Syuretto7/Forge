import sub


def test_intervals():
    lo, hi = sub.wald(50, 100)
    assert abs(lo - 0.402) < 1e-12 and abs(hi - 0.598) < 1e-12
    lo, hi = sub.wilson(0, 20)
    assert lo < 1e-12 and 0.15 < hi < 0.17
    lo, hi = sub.credible(0, 20)
    assert lo < 0.002 and 0.15 < hi < 0.17


def test_rare_event_coverage():
    assert sub.exact_coverage(sub.wald, 0.05, 20) < 0.7
    assert sub.exact_coverage(sub.wilson, 0.05, 20) > 0.9
    assert sub.exact_coverage(sub.credible, 0.05, 20) > 0.9


def test_easy_case():
    for f in (sub.wald, sub.wilson, sub.credible):
        assert 0.93 < sub.exact_coverage(f, 0.5, 100) < 0.96
