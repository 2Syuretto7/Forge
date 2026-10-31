# Adam, and the Rosenbrock valley

1. `rosenbrock_fg(p, a=1, b=100)` returns the value and gradient of $f(x, y) = (a - x)^2 + b(y - x^2)^2$, a curved valley whose minimum is at $(a, a^2)$.
2. `Adam(lr, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True)` with a method `step(x, g)` that returns the updated array. It keeps $m$, $v$ and the step count $t$ between calls.

Then run your Adam on the Rosenbrock valley and compare it with gradient descent at the largest rate that stays stable.

## Hints

1. $\partial f/\partial x = -2(a - x) - 4bx(y - x^2)$ and $\partial f/\partial y = 2b(y - x^2)$.
2. Initialize $m$ and $v$ to zeros of the gradient's shape on the first call, and increment $t$ before using it in $1 - \beta^t$.
3. `step` returns `x - lr * m_hat / (sqrt(v_hat) + eps)` and must not modify `x` in place.
