# Break it: a solver that breaks complementary slackness

Three candidate answers for the same small quadratic program arrive from three solvers (the starter's `CANDIDATES`), each a point and its multipliers. One is right; one puts a positive multiplier on a constraint that is not active; one returns a point that violates a constraint. Find them from the KKT residuals alone (Section 2).

The problem (the starter's `problem()`): minimize $\frac12\lVert x - c\rVert^2$ subject to $Gx \le h$.

- `residuals(x, lam)`: the dict of e02's four residuals for this problem.
- `diagnose(x, lam, tol=1e-6)`: `"optimal"` if all residuals are within `tol`, else the name of the largest residual among `"stationarity"`, `"primal"`, `"dual"` and `"slackness"`.

## Hints

1. Here $\nabla f = x - c$ and the constraint gradients are the rows of $G$.
2. A positive multiplier on an inactive constraint shows up twice: in slackness, and in stationarity, since it pushes on a constraint that is not there.
3. The diagnosis names a symptom; the bug is in the solver that produced it.
