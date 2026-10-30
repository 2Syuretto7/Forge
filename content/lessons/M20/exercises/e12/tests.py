import sub


def test_counts():
    assert sub.grid_points(2, 1e-4) == 10 ** 4
    assert sub.mc_points(1e-4) == 10 ** 8
    assert sub.crossover_dimension(1e-4) == 5
    assert sub.grid_points(10, 1e-4) == 10 ** 20
