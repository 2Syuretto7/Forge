# Fibonacci from two eigenvalues

$\begin{pmatrix} F_{n+1} \\ F_n \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n \begin{pmatrix} 1 \\ 0 \end{pmatrix}$. The matrix has eigenvalues $\varphi = (1 + \sqrt 5)/2$ and $\psi = (1 - \sqrt 5)/2$, and diagonalizing it gives Binet's formula $F_n = (\varphi^n - \psi^n)/\sqrt 5$.

- `fib_power(n)`: $F_n$ exactly, by raising the matrix to the $n$-th power with Python integers and repeated squaring (M05).
- `fib_binet(n)`: Binet's formula in floating point, rounded to the nearest integer.
- `first_disagreement(limit=100)`: the first $n$ at which the two differ.

## Hints

1. Represent a 2 by 2 integer matrix as a tuple of four ints and write its product by hand.
2. Squaring: if $n$ is even, $M^n = (M^{n/2})^2$; if odd, multiply by one more $M$.
3. Floats carry about 16 digits; $F_{80}$ has 17.
