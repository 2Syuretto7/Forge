# Rotation has no real eigenvector

- `eig2_complex(A)`: the two eigenvalues of a 2 by 2 real matrix as Python complex numbers, from the quadratic formula with `cmath.sqrt`.
- `rotation_scale(A)`: for a matrix of the form $r \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$, return `(r, theta_degrees)` read off the eigenvalue $r e^{i\theta}$ with positive imaginary part.
- `orbit_norms(A, x0, k)`: the lengths of $A^j x_0$ for $j = 0, \dots, k$.

A real vector multiplied by a rotation keeps turning; power iteration never settles, but the lengths grow exactly like $r^j$.

## Hints

1. `cmath.sqrt` of a negative number is imaginary.
2. `abs(z)` and `math.degrees(cmath.phase(z))`.
3. Multiply repeatedly and record `np.linalg.norm`.
