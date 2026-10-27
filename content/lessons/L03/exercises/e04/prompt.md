# A numerical Jacobian

Extend the checker to vector outputs. For `f` mapping a 1-D array of length $n$ to a 1-D array of length $m$:

- `numerical_jacobian(f, x, h)` returns the $m \times n$ matrix of central differences, $J_{ij} \approx \partial f_i/\partial x_j$: column $j$ comes from perturbing input $j$.
- `jacobian_of_composition(Jg, Jf)` returns the Jacobian of $g \circ f$ from the two Jacobians (Section 3).

## Hints

1. Column `j` is `(f(x + h e_j) - f(x - h e_j)) / (2h)`.
2. Determine $m$ from one evaluation of `f`.
3. The chain rule is a single matrix product, in the right order.
