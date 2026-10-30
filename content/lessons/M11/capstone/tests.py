import numpy as np
import sub

TESTS = sub.make_tests()


def test_forty_systems():
    assert len(TESTS) == 40
    for k, (name, A, b, status, r) in enumerate(TESTS):
        out = sub.solve(A, b)
        assert out["rank"] == r, f"system {k} ({name}): rank {out['rank']}, expected {r}"
        assert out["status"] == status, f"system {k} ({name}): {out['status']}, expected {status}"
        if status == "none":
            assert out["x"] is None and out["residual"] > 1e-3
        else:
            x = out["x"]
            assert np.isclose(out["residual"], np.linalg.norm(A @ x - b), rtol=1e-6, atol=1e-15)
            assert out["residual"] <= 1e-9 * (np.linalg.norm(A) * np.linalg.norm(x) + np.linalg.norm(b))


def test_unique_solutions_are_right():
    rng = np.random.default_rng(9)
    A = rng.normal(size=(6, 6))
    x0 = rng.normal(size=6)
    assert np.allclose(sub.solve(A, A @ x0)["x"], x0)


def test_edge_cases():
    assert sub.solve(np.zeros((2, 3)), np.zeros(2))["status"] == "infinite"
    assert sub.solve(np.zeros((2, 3)), np.ones(2))["status"] == "none"
    out = sub.solve(np.array([[1e-20, 1.0], [1.0, 1.0]]), np.array([1.0, 2.0]))
    assert out["status"] == "unique" and np.allclose(out["x"], [1, 1])
