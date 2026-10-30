# Grids against samples in many dimensions

Integrate over $[0, 1]^d$ to an error `tol`:

- `grid_points(d, tol, C=1.0)`: a midpoint grid with $m$ points per axis has error about $C/m^2$, so $m = \lceil\sqrt{C/\text{tol}}\,\rceil$ and the grid has $m^d$ points.
- `mc_points(tol, sigma=1.0)`: Monte Carlo with standard deviation `sigma` needs $\lceil(\sigma/\text{tol})^2\rceil$ samples, in any dimension.
- `crossover_dimension(tol, C=1.0, sigma=1.0)`: the smallest $d$ for which the grid needs more points than Monte Carlo.

## Hints

1. `math.ceil` and integer powers.
2. For `tol = 1e-4`: 100 points per axis, so $100^d$, against $10^8$ samples.
3. Loop $d = 1, 2, \dots$
