# Capstone: a gradient-check harness

The starter's `SUITE` lists 25 entries `(name, f, jac, n, positive)`: `f` maps an array of length `n` to an array (a scalar function returns an array of length 1), `jac` is its hand-written Jacobian, and `positive` says the inputs must be positive. Some of the Jacobians are wrong.

1. `numerical_jacobian(f, x)`: central differences with a step scaled to each input, $h_j = \varepsilon^{1/3}\max(1, |x_j|)$.
2. `relative_error(A, B)`: $\|A - B\| / \max(\|A\| + \|B\|, 10^{-12})$ (Frobenius).
3. `check(entry, points=5, seed=0)`: the worst relative error over `points` random inputs drawn from `np.random.default_rng(seed)` (standard normal, or uniform on $[0.5, 2]$ when `positive`).
4. `run_suite(tol=1e-6)`: the sorted list of names whose worst error exceeds `tol`.

The tests require `run_suite` to name exactly the planted bugs, and every correct Jacobian to pass with a worst error below $10^{-6}$ (most are near $10^{-10}$).
