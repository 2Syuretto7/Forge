# How fast CG converges

After $k$ steps CG has the best approximation in the **Krylov subspace** $\mathrm{span}\{b, Ab, \dots, A^{k-1}b\}$, measured in the $A$-norm, so its error is $\min_q\lVert q(A)e_0\rVert_A$ over polynomials of degree $k$ with $q(0) = 1$ (Section 3). Two consequences: with only $d$ distinct eigenvalues, CG finishes in $d$ steps, because a degree-$d$ polynomial can vanish on all of them; and with condition number $\kappa$, Chebyshev polynomials give

$$
\frac{\lVert e_k\rVert_A}{\lVert e_0\rVert_A} \le 2\left(\frac{\sqrt\kappa - 1}{\sqrt\kappa + 1}\right)^k .
$$

- `cg_iterations(A, b, tol=1e-8)`: the number of CG iterations to reach the relative residual `tol` (write your own CG or reuse e04's).
- `cg_bound(kappa, k)`: the right-hand side above.
- `iterations_predicted(kappa, tol)`: the smallest $k$ with `cg_bound(kappa, k)` $\le$ `tol`.
- `spd_with_spectrum(eigenvalues, rng)`: $Q\,\mathrm{diag}(\lambda)\,Q^\top$ with $Q$ a random orthogonal matrix from the QR factorization of a Gaussian matrix.

The tests find the iteration count growing like $\sqrt\kappa$, staying below the prediction, and dropping to 5 for a $200 \times 200$ matrix with five distinct eigenvalues.

## Hints

1. Gradient descent needs about $\kappa$ steps; CG needs about $\sqrt\kappa$. That square root is the whole point of the method.
2. The bound is about the $A$-norm of the error, the test about the residual; for these matrices the prediction still holds with room to spare.
3. Use `np.linalg.qr(rng.standard_normal((n, n)))[0]` for $Q$.
