# Jacobians of common layers

Write each Jacobian in closed form:

- `jac_affine(W)`: of $x \mapsto Wx + b$.
- `jac_tanh(x)`: of the elementwise $\tanh$: $\operatorname{diag}(1 - \tanh^2 x)$.
- `jac_softmax(z)`: of $p = \operatorname{softmax}(z)$: $\operatorname{diag}(p) - pp^\top$.
- `jac_polar(v)`: of $(r, \theta) \mapsto (r\cos\theta, r\sin\theta)$ at `v = [r, theta]`.
- `jac_normalize(x)`: of $x \mapsto x / \|x\|$: $\frac{1}{\|x\|}\big(I - \frac{xx^\top}{\|x\|^2}\big)$.

The tests run a **gradient check** of each against a numerical Jacobian (provided).

## Hints

1. The softmax Jacobian's rows sum to zero: adding a constant to every logit changes nothing.
2. The polar Jacobian's determinant is $r$ (M20 uses it).
3. Normalizing kills the radial direction: $J x = 0$.
