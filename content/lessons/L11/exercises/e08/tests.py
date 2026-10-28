import sub


def test_transfer_time():
    assert abs(sub.transfer_time(64 * 2 ** 20, 12e9) - (10e-6 + 64 * 2 ** 20 / 12e9)) < 1e-15
    assert abs(sub.effective_bandwidth(120_000, 12e9) - 6e9) < 1


def test_pipeline():
    mb = 4 * 2 ** 20
    t_copy = sub.transfer_time(mb, 12e9)
    assert abs(sub.input_pipeline_time(mb, 1e-3, 12e9, overlap=False) - (t_copy + 1e-3)) < 1e-15
    assert sub.input_pipeline_time(mb, 1e-3, 12e9, overlap=True) == 1e-3
    assert sub.input_pipeline_time(mb, 1e-4, 12e9, overlap=True) == t_copy
