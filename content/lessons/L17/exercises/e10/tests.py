import sub


def test_amdahl():
    assert abs(sub.amdahl_speedup([0.5, 0.5], [2, 2]) - 2) < 1e-12
    assert abs(sub.amdahl_speedup([0.7, 0.3], [1e9, 2]) - 1 / 0.15) < 1e-6


def test_t4():
    mm, mem = sub.t4_part_speedups()
    assert abs(mm - 65 / 8.1) < 1e-12 and mem == 2.0
    s = sub.amdahl_speedup([0.7, 0.3], [mm, mem])
    assert 4.0 < s < 4.3
