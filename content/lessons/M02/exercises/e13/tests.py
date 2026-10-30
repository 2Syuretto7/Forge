import sub


def test_factoring_finds_both():
    assert sub.solve_by_factoring(4) == [0, 4]
    assert sub.solve_by_factoring(-3) == [-3, 0]
    assert sub.solve_by_factoring(0) == [0]


def test_dividing_loses_zero():
    assert sub.solve_by_dividing(4) == [4]
    assert sub.lost_solutions(4) == [0]
    assert sub.lost_solutions(0) == []


def test_every_reported_solution_checks():
    for k in [-5, -1, 0, 2, 9]:
        for x in sub.solve_by_factoring(k):
            assert sub.is_solution(k, x)
        for x in sub.lost_solutions(k):
            assert sub.is_solution(k, x), "a lost solution is still a solution"
