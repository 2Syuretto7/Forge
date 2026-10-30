# Capstone: a robust linear solver

Write `solve(A, b, tol=None)` for any `m` by `n` matrix. It returns a dictionary:

- `"rank"`: the numerical rank, by elimination with complete pivoting and the default tolerance `max(m, n) * 1e-12 * max|a_ij|`;
- `"status"`: `"unique"`, `"infinite"` or `"none"`;
- `"x"`: a solution (free variables at 0) or `None`;
- `"residual"`: $\|Ax - b\|$ for the returned `x`, or, when there is no solution, $\|A\hat x - b\|$ for the $\hat x$ that satisfies the pivot equations (how badly the remaining equations disagree).

Decide consistency from the residual of that candidate, relative to the size of the problem: consistent when $\|A\hat x - b\| \leq 10^{-9} (\|A\|_F \|\hat x\| + \|b\|)$.

The starter's `make_tests()` builds 40 systems in eight families (well conditioned, needing row swaps, nearly singular, singular and consistent, singular and inconsistent, tall and consistent, tall and inconsistent, wide), each with its expected status and rank. Your solver must get every one right.
