# Jacobian determinants

- `jacobian_det(T, p, h=1e-6)`: the determinant of the central-difference Jacobian of a map `T` from $\mathbb{R}^n$ to $\mathbb{R}^n$ at `p`.
- `det_polar(r, theta)`: $r$.
- `det_spherical(r, phi, theta)`: $r^2\sin\phi$, for $x = r\sin\phi\cos\theta$, $y = r\sin\phi\sin\theta$, $z = r\cos\phi$.
- `det_box_muller(u1, u2)`: the absolute Jacobian determinant of the Box-Muller map, $2\pi/u_1$.

The tests run **gradient checks** of each formula against `jacobian_det`.

## Hints

1. Build the matrix column by column, then `np.linalg.det`.
2. Write the maps as functions of a NumPy array of coordinates.
3. Box-Muller: $(u_1, u_2) \mapsto \sqrt{-2\ln u_1}\,(\cos 2\pi u_2, \sin 2\pi u_2)$.
