# Explain it plainly: no bad minima

Explain why convex problems have no bad local minima.

Guidelines:

- Write 150 to 400 words.
- Use the picture of a bowl and of a chord.
- Say what can go wrong without convexity, with an example.
- Say what this buys you in practice.

:::feynman{id=f1 prompt="Explain why convex problems have no bad local minima." key_points="A convex function lies on or below the chord between any two points of its graph|If some point were lower than a local minimum, the chord from the local minimum to it would slope down, and convexity would put nearby points on the segment below the local minimum|That contradicts being a local minimum, so every local minimum is global|Equivalently, a convex differentiable function lies above its tangent planes, so a zero gradient certifies the global minimum|Without convexity, as in a double well, gradient descent ends in whichever basin the start drains into, which may be the worse one"}
:::

## A written proof

:::feynman{id=proof1 prompt="For f(x) = (1/2) x^T A x with A symmetric positive definite and eigenvalues mu = lambda_min <= ... <= lambda_max = L, prove that gradient descent with step eta multiplies the component of the error along each eigenvector by 1 - eta lambda_i, and that it converges for every starting point exactly when 0 < eta < 2/L." key_points="Computes the gradient A x and writes the update x_{k+1} = (I - eta A) x_k, the error being x itself since the minimum is 0|Expands x_k in the orthonormal eigenvector basis of A, by the spectral theorem|Shows each coefficient is multiplied by 1 - eta lambda_i per step, so after k steps by (1 - eta lambda_i)^k|Notes convergence for every start requires |1 - eta lambda_i| < 1 for every i|Solves the inequalities: they hold for all i exactly when 0 < eta < 2/lambda_max = 2/L"}
:::
