# Nearly repeated sensors

Two sensors, the second nearly a copy of the first: $A = \begin{pmatrix} 1 & 1 \\ 1 & 1 + \delta \end{pmatrix}$, readings $b = (2, 2 + \delta)$, true loads $x = (1, 1)$.

- `system(delta)`: return `(A, b)`.
- `amplification(delta, db)`: change the second reading by `db`, solve again (any solver), and return $\|\Delta x\| / |db|$.
- `cond_inf(A)`: the condition number in the infinity norm, $\|A\|_\infty \|A^{-1}\|_\infty$, where $\|M\|_\infty$ is the largest row sum of absolute values (use `np.linalg.inv` for the inverse).

The tests check an **invariant**: for random perturbations $\Delta b$, the relative change of the solution is at most `cond_inf(A)` times the relative change of the readings, both measured in the infinity norm.

## Hints

1. Solving by hand: $\Delta x = db \cdot (-1, 1) / \delta$, so the amplification is $\sqrt{2}/\delta$.
2. `np.max(np.sum(np.abs(M), axis=1))`.
3. $\|\Delta x\| / \|x\| \leq \kappa\, \|\Delta b\| / \|b\|$ follows from $\Delta x = A^{-1} \Delta b$ and $\|b\| \leq \|A\|\,\|x\|$.
