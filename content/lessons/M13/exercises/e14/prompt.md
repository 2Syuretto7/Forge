# Too few eigenvectors

- `is_diagonalizable(A, tol=1e8)`: whether the eigenvector matrix from `np.linalg.eig` is invertible in practice (its condition number below `tol`); over the complex numbers, so a rotation counts.
- `shear_power(k)`: $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}^k$ by $k$ multiplications.
- `angle_after(k)`: the angle in degrees between $(1, 0)$, the shear's one eigenvector, and $A^k (0, 1)$.

## Hints

1. `np.linalg.cond(V)`; for a defective matrix the two computed eigenvectors are nearly parallel and the condition number is enormous.
2. The powers have $k$ in the corner: growth like $k$, not like an eigenvalue to the $k$.
3. $A^k (0, 1) = (k, 1)$, so the angle is $\arctan(1/k)$: about 2.9 degrees after 20 steps, against $10^{-9}$ degrees for a gap like 3 to 1.
