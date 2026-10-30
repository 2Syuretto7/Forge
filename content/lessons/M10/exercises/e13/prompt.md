# The order of a pipeline

A pipeline is a list of 3 by 3 homogeneous matrices in the order they are applied.

- `pipeline_matrix(steps)`: the single matrix of the pipeline.
- `commutes(A, B, tol=1e-12)`: whether $AB = BA$ up to `tol`.
- `place_logo()`: return a pipeline (a list of matrices) that takes the unit square $[0, 1]^2$, rotates it by $45^\circ$ about its own centre $(0.5, 0.5)$, and then moves it so its centre lands at $(3, 2)$. The common bug, rotating about the origin after moving, puts it somewhere else; the tests check where the centre lands.

## Hints

1. The first step must stand rightmost: `steps[-1] @ ... @ steps[0]`.
2. Rotation about the centre: translate by $-c$, rotate, translate by $+c$.
3. Then translate by $(3, 2) - (0.5, 0.5)$.
