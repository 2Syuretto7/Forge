# Classical Gram-Schmidt forgets

- `cgs(A)`: classical Gram-Schmidt, every coefficient computed from the **original** column: `R[j, k] = Q[:, j] @ A[:, k]`.
- `mgs(A)`: modified Gram-Schmidt (e03), each coefficient from the running vector.
- `cgs2(A)`: classical Gram-Schmidt run twice on each column (orthogonalize, then orthogonalize the result again), the usual fix.
- `loss_of_orthogonality(Q)`: $\|Q^\top Q - I\|$ (Frobenius).

`ill(kappa, seed=0)` in the starter builds a $40 \times 8$ matrix with condition number `kappa`. At $\kappa = 10^{8}$, classical Gram-Schmidt's columns are far from orthogonal, modified is off by about $\kappa \varepsilon$, and the twice-run classical version is orthogonal to rounding.

## Hints

1. The only difference between `cgs` and `mgs` is which vector the coefficient is computed from.
2. For `cgs2`, after the first pass compute `w = v - Q[:, :k] @ (Q[:, :k].T @ v)` again.
3. `np.linalg.norm(Q.T @ Q - np.eye(n))`.
