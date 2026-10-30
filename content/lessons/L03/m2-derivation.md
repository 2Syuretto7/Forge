# Derivation: derivatives as linear maps, and how to compute them

The plan: understand the error of finite differences through Taylor's theorem; generalize the derivative to functions of many variables (gradients and Jacobians); state the chain rule for them; see that it can be evaluated in two orders, forward and reverse, with very different costs; implement forward mode with dual numbers; derive the Jacobians of the three operations that dominate deep learning; and finish with the Taylor argument for why gradient descent works.

## 1. Taylor's theorem and the error of finite differences

If $f$ is smooth near $x$, then for small $h$

$$
f(x + h) = f(x) + f'(x)\,h + \tfrac{1}{2} f''(x)\,h^2 + \tfrac{1}{6} f'''(x)\,h^3 + O(h^4).
$$

Divide the expansion by $h$ to read off the error of the **forward difference**: $\dfrac{f(x+h) - f(x)}{h} = f'(x) + \tfrac{1}{2} f''(x)\,h + O(h^2)$. Its **truncation error** is about $\tfrac{1}{2}|f''|\,h$: first order in $h$.

The **central difference** cancels the even terms:

$$
\frac{f(x + h) - f(x - h)}{2h} = f'(x) + \tfrac{1}{6} f'''(x)\, h^2 + O(h^4).
$$

Its truncation error is second order: halving $h$ divides it by four.

Floating point adds a second error. Each evaluation of $f$ is off by about $\varepsilon |f(x)|$ with $\varepsilon \approx 1.1 \times 10^{-16}$ in float64. The difference of two such values carries that error, and dividing by $h$ amplifies it: the **rounding error** is about $\varepsilon |f| / h$.

::::derivation{id=d1 title="The best step size"}
:::step
For the forward difference, write the total error as $E(h) = a h + b/h$ with $a = |f''|/2$ and $b = \varepsilon |f|$. Its derivative is $E'(h) = a -$ [[b/h^2]].
:::
:::step
Setting $E'(h) = 0$ gives the optimal step $h^\star =$ [[sqrt(b/a)]], which is of order $\sqrt{\varepsilon} \approx 10^{-8}$ when $f$ and $f''$ are of order one.
:::
:::step
At the optimum the error is $E(h^\star) = 2\sqrt{ab}$, of order $\sqrt{\varepsilon}$. So the forward difference can never be trusted beyond about [[8]] significant digits in float64.
:::
:::step
For the central difference, $E(h) = c h^2 + b/h$ with $c = |f'''|/6$. Setting the derivative to zero gives $2 c h = b / h^2$, so $h^\star = (b / (2c))^{1/3}$, of order $\varepsilon^{1/3}$. In float64 that is about $10^{-5}$, and the best error is of order $\varepsilon^{2/3} \approx$ [[2e-11|tol=1.5e-11]].
:::
::::

This is the answer to the puzzle: at $h = 10^{-12}$ the rounding term $\varepsilon e / h \approx 3 \times 10^{-4}$ dominates. For gradient checks in this course we use central differences with $h \approx 10^{-6}$ in float64: truncation about $10^{-12}$, rounding about $10^{-10}$, comfortably below the $10^{-5}$ tolerance.

## 2. Many variables: partial derivatives and the gradient

For $f: \mathbb{R}^n \to \mathbb{R}$, the **partial derivative** $\partial f / \partial x_j$ is the ordinary derivative along coordinate $j$ with the others held fixed. The **gradient** collects them, $\nabla f(x) = \big(\partial f/\partial x_1, \dots, \partial f/\partial x_n\big)$, and gives the best linear approximation

$$
f(x + h) \approx f(x) + \nabla f(x)^\top h .
$$

Two facts follow. The **directional derivative** along a unit vector $v$ is $\nabla f^\top v$. By Cauchy-Schwarz it is largest when $v$ points along $\nabla f$, so the gradient is the direction of steepest ascent, and $-\nabla f$ the direction of steepest descent.

## 3. Vector outputs: the Jacobian

For $f: \mathbb{R}^n \to \mathbb{R}^m$, the derivative is the $m \times n$ **Jacobian** matrix $J_{ij} = \partial f_i / \partial x_j$, and

$$
f(x + h) \approx f(x) + J(x)\, h .
$$

The Jacobian is the derivative: the linear map that best approximates $f$ near $x$. Row $i$ is the gradient of output $i$; column $j$ is how all outputs respond to input $j$.

**Chain rule.** If $y = f(x)$ and $z = g(y)$, then to first order $\delta z \approx J_g \delta y \approx J_g J_f \delta x$, so

$$
J_{g \circ f}(x) = J_g\big(f(x)\big)\; J_f(x).
$$

The Jacobian of a composition is the product of Jacobians. A deep network is a long composition, so its derivative is a long matrix product: $J = J_L J_{L-1} \cdots J_1$.

::::derivation{id=d2 title="A small Jacobian by hand"}
:::step
Let $f(x_1, x_2) = (x_1 x_2,\; \sin x_1)$. The first row of the Jacobian is $(x_2, x_1)$. The entry $\partial f_2 / \partial x_1$ is [[cos(x1)]].
:::
:::step
The entry $\partial f_2 / \partial x_2$ is [[0]].
:::
:::step
Now let $g(y_1, y_2) = y_1 + y_2$, so $J_g = (1, 1)$, and $h(x) = g(f(x)) = x_1 x_2 + \sin x_1$. By the chain rule, $\partial h / \partial x_1 = 1 \cdot x_2 + 1 \cdot \cos x_1$, which is the sum of column one of $J_f$. At $x = (0, 3)$ it equals [[4]].
:::
::::

## 4. Two ways to multiply a chain of Jacobians

For a loss $L = \ell(f_L(\cdots f_1(x)))$ we need $\nabla_x L$, a row of the product $J_\ell J_L \cdots J_1$. Matrix multiplication is associative, so we can choose the order.

**Forward mode** multiplies from the right. Start with a direction $v$ in input space and push it through: $v_1 = J_1 v$, $v_2 = J_2 v_1$, and so on. Each step is a **Jacobian-vector product** (JVP). One pass gives $J v$, the directional derivative of every output along one input direction. A full gradient with respect to $n$ inputs needs $n$ passes.

**Reverse mode** multiplies from the left. Start with $u = \partial L / \partial L = 1$ at the output and pull it back: $u_L = u^\top J_\ell$, then $u_{L-1} = u_L^\top J_L$, and so on. Each step is a **vector-Jacobian product** (VJP). One pass gives a full row: the gradient of one output with respect to every input.

::::derivation{id=d3 title="Counting passes"}
:::step
For a function $\mathbb{R}^n \to \mathbb{R}^m$, forward mode needs one pass per input to build the full Jacobian: [[n]] passes.
:::
:::step
Reverse mode needs one pass per output: [[m]] passes.
:::
:::step
Training computes the gradient of one scalar loss with respect to $n = 10^9$ parameters. Forward mode needs $10^9$ passes; reverse mode needs [[1]].
:::
::::

Each pass costs a small constant times one evaluation of $f$, so reverse mode delivers the entire gradient of a scalar for a few times the cost of computing the scalar. This is the **cheap gradient principle**, and **backpropagation** is reverse mode applied to a neural network. The price: reverse mode must remember the intermediate values of the forward pass to evaluate the local Jacobians on the way back. That memory is the activation memory of L08 and L18.

:::edge{to=L07 text="Backpropagation through an MLP: reverse mode with one VJP per layer."}
:::

:::edge{to=L08 text="You will implement reverse mode as an autograd engine with a tape of saved tensors."}
:::

## 5. Forward mode with dual numbers

Forward mode has an elegant implementation. A **dual number** is $a + b\epsilon$ with the rule $\epsilon^2 = 0$. Taylor's theorem then terminates after one term:

$$
f(a + b\epsilon) = f(a) + f'(a)\, b\, \epsilon .
$$

So if you evaluate a program on $x + 1\cdot\epsilon$ instead of $x$, the $\epsilon$ part of the result is exactly $f'(x)$, with no step size and no truncation. You only need arithmetic rules for duals.

::::derivation{id=d4 title="Arithmetic on dual numbers"}
:::step
Sum: $(a + b\epsilon) + (c + d\epsilon) = (a + c) + (b + d)\epsilon$. Product: $(a + b\epsilon)(c + d\epsilon) = ac + (ad + bc)\epsilon + bd\,\epsilon^2$. The $\epsilon$ coefficient of the product is [[a*d + b*c]], which is the product rule.
:::
:::step
Quotient: $\dfrac{a + b\epsilon}{c + d\epsilon} = \dfrac{a}{c} + q\,\epsilon$. Multiply both sides by $c + d\epsilon$ and match $\epsilon$ terms to find $q =$ [[(b*c - a*d)/c^2]].
:::
:::step
Functions: $\sin(a + b\epsilon) = \sin a + b \cos a\,\epsilon$, and in general $g(a + b\epsilon) = g(a) + g'(a)\, b\,\epsilon$. For $g = \exp$ the $\epsilon$ coefficient is [[b*exp(a)]].
:::
:::step
Example: $f(x) = x \sin x$ at $x = a$. Evaluating on $a + \epsilon$ gives $\epsilon$ coefficient $\sin a + a \cos a$. At $a = 0$ that is [[0]].
:::
::::

A dual number carries one directional derivative through the computation alongside the value. For a function of $n$ inputs, seed input $j$ with $\epsilon$ and the others with $0$, and repeat for each $j$: that is $n$ forward passes, exactly as counted above. You will build a dual-number library and use it in the capstone.

## 6. The three Jacobians that matter most

Most of a neural network's computation is matrix multiplication, softmax and normalization. Their VJPs are worth knowing by heart.

**Matrix multiplication.** Let $Y = XW$ with $X \in \mathbb{R}^{B \times n}$ and $W \in \mathbb{R}^{n \times m}$, and let $G = \partial L / \partial Y$ be the upstream gradient. Since $Y_{bj} = \sum_k X_{bk} W_{kj}$, we have $\partial L / \partial X_{bk} = \sum_j G_{bj} W_{kj}$ and $\partial L / \partial W_{kj} = \sum_b X_{bk} G_{bj}$:

$$
\frac{\partial L}{\partial X} = G W^\top, \qquad \frac{\partial L}{\partial W} = X^\top G .
$$

A useful check: each gradient has the shape of the thing it differentiates, and there is only one way to multiply the available matrices to get that shape.

**Softmax.** For $p = \operatorname{softmax}(z)$ with $p_i = e^{z_i} / \sum_k e^{z_k}$:

::::derivation{id=d5 title="The softmax Jacobian"}
:::step
Write $p_i = e^{z_i}/S$ with $S = \sum_k e^{z_k}$. For $i = j$, the quotient rule gives $\partial p_i / \partial z_i = \dfrac{e^{z_i} S - e^{z_i} e^{z_i}}{S^2} = p_i - p_i^2$. With $p_i = 0.2$ this is [[0.16]].
:::
:::step
For $i \neq j$ only the denominator depends on $z_j$, so $\partial p_i / \partial z_j = -e^{z_i} e^{z_j} / S^2 =$ [[-a*b]], writing a for $p_i$ and b for $p_j$.
:::
:::step
Together, $J = \operatorname{diag}(p) - p p^\top$. Each column sums to $p_j - p_j \sum_i p_i =$ [[0]]: adding a constant to every logit leaves the softmax unchanged.
:::
::::

The VJP never needs the $K \times K$ matrix: $u^\top J = p \odot (u - u^\top p)$, an $O(K)$ computation. With a vocabulary of 50,000 tokens the full Jacobian would have 2.5 billion entries.

:::edge{to=L04 text="Compose the softmax VJP with the gradient of -log p_y and you get the famous p - onehot(y)."}
:::

**Layer normalization.** For $x \in \mathbb{R}^d$, let $\mu = \frac{1}{d}\sum_i x_i$, $\sigma = \sqrt{\frac{1}{d}\sum_i (x_i - \mu)^2 + \varepsilon}$, and $\hat x = (x - \mu)/\sigma$. Differentiating carefully (both $\mu$ and $\sigma$ depend on every $x_i$) gives, with $\varepsilon = 0$,

$$
\frac{\partial \hat x}{\partial x} = \frac{1}{\sigma}\Big(I - \tfrac{1}{d}\mathbf{1}\mathbf{1}^\top - \tfrac{1}{d}\hat x \hat x^\top\Big), \qquad
u^\top \frac{\partial \hat x}{\partial x} = \frac{1}{\sigma}\Big(u - \bar u\,\mathbf{1} - \overline{u \odot \hat x}\; \hat x\Big)^\top ,
$$

where bars denote means over the $d$ coordinates. The two subtracted terms remove the directions to which $\hat x$ is blind: shifting $x$ by a constant (the $\mathbf{1}$ direction) and scaling it (the $\hat x$ direction). You will verify both invariances numerically; L10 builds normalization layers on this formula.

## 7. Why gradient descent works, locally

Take a step against the gradient: $x' = x - \eta g$ with $g = \nabla f(x)$. Second-order Taylor with Hessian $H$ gives

$$
f(x') = f(x) - \eta \|g\|^2 + \tfrac{1}{2}\eta^2 g^\top H g + O(\eta^3).
$$

The first-order term always decreases $f$; the second-order term may increase it. If the curvature is bounded, $g^\top H g \le L \|g\|^2$, then

::::derivation{id=d6 title="A guaranteed decrease"}
:::step
$f(x') \le f(x) - \eta \|g\|^2 + \tfrac{1}{2} L \eta^2 \|g\|^2$ (ignoring higher-order terms, which vanish exactly for quadratics). The decrease $\eta - \tfrac{1}{2}L\eta^2$, per unit of $\|g\|^2$, is positive whenever $0 < \eta <$ [[2/L]].
:::
:::step
It is largest at $\eta = 1/L$, where the decrease equals $\|g\|^2 / (2L)$. With $\|g\|^2 = 8$ and $L = 4$, one step lowers $f$ by at least [[1]].
:::
:::step
For the quadratic $f(x) = \tfrac{1}{2} L x^2$ in one dimension, a step $x' = x - \eta L x = (1 - \eta L) x$. With $\eta = 2.5/L$, $|1 - \eta L| =$ [[1.5]], so the iterates grow: the step is too large and gradient descent diverges.
:::
::::

So gradient descent is a sequence of trusted local linear approximations, and the step size must respect the curvature. L09 turns this into convergence rates and shows that the condition number $L/\mu$ from M14 controls how many steps you need.

## Summary

| Idea | Formula | Where it comes back |
| --- | --- | --- |
| Central difference | error $\tfrac{1}{6}|f'''|h^2 + \varepsilon|f|/h$ | every gradient check |
| Jacobian chain rule | $J_{g\circ f} = J_g J_f$ | backprop (L07) |
| Reverse mode | one VJP per layer, one pass per output | autograd (L08) |
| Dual numbers | $f(a + \epsilon) = f(a) + f'(a)\epsilon$ | forward-mode tools |
| Matmul VJP | $G W^\top$, $X^\top G$ | every linear layer |
| Softmax Jacobian | $\operatorname{diag}(p) - pp^\top$ | cross-entropy (L04), attention (L13) |
| Descent lemma | $\eta < 2/L$ | learning rates (L09) |
