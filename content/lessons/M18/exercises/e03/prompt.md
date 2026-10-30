# A numerical Jacobian

For `f` mapping a 1-D array of length $n$ to a 1-D array of length $m$:

- `numerical_jacobian(f, x, h=1e-6)`: the $m \times n$ matrix of central differences, $J_{ij} \approx \partial f_i / \partial x_j$; column $j$ comes from perturbing input $j$.
- `jacobian_of_composition(Jg, Jf)`: the Jacobian of $g \circ f$ from the two Jacobians.

The tests run **gradient checks**: a linear map's Jacobian is its matrix, an elementwise function's is diagonal, and the chain rule holds numerically.

## Hints

1. Column `j` is `(f(x + h e_j) - f(x - h e_j)) / (2h)`.
2. Determine $m$ from one evaluation of `f`.
3. The chain rule is one matrix product, in the right order.
