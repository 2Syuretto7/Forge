# Derivation: matrix calculus and automatic differentiation

## 1. Derivatives of matrix expressions

To differentiate a scalar $L$ with respect to a matrix $W$, perturb $W$ by a small $E$, keep the first-order change, and read off the matrix that pairs with $E$: if $\delta L = \sum_{ij} G_{ij} E_{ij}$, then $\partial L/\partial W = G$, a matrix of the same shape as $W$.

For a layer $Y = XW$ ($X$ is $B \times n$, $W$ is $n \times m$) with upstream gradient $G = \partial L/\partial Y$ ($B \times m$): $\delta Y = X E$, so $\delta L = \sum_{bj} G_{bj}(XE)_{bj} = \sum_{ij} (X^\top G)_{ij} E_{ij}$. Hence

$$
\frac{\partial L}{\partial W} = X^\top G, \qquad \frac{\partial L}{\partial X} = G W^\top .
$$

The shapes check themselves: $X^\top G$ is $n \times m$ like $W$, and $GW^\top$ is $B \times n$ like $X$.

::::derivation{id=d1 title="Shapes of matmul gradients"}
:::step
With a batch of $B = 32$, $n = 64$ inputs and $m = 10$ outputs, $\partial L/\partial W = X^\top G$ has [[640]] entries.
:::
:::step
Computing it costs $2Bnm$ operations, the same as the forward product. The backward pass of a matmul layer computes two such products, so its cost is about [[2]] times the forward pass.
:::
::::

## 2. Jacobian-vector and vector-Jacobian products

A Jacobian $J$ ($m \times n$) is rarely formed. Two products are cheap without it:

- the **JVP** $Jv$: how all outputs move when the input moves in direction $v$;
- the **VJP** $u^\top J$: how a weighting $u$ of the outputs changes with each input.

For an elementwise $\tanh$, $Jv = (1 - y^2) \odot v$ and $u^\top J = u \odot (1 - y^2)$: $O(n)$ instead of $O(n^2)$. For the softmax, $u^\top J = p \odot (u - u \cdot p)$, again $O(n)$.

## 3. Computational graphs

A program that computes $f$ is a directed acyclic graph: inputs at the bottom, each node an elementary operation of earlier nodes, the output at the top. Every node has local derivatives with respect to its arguments, known in closed form. The chain rule over the graph says: the derivative of the output with respect to a node is the **sum over all paths** from that node to the output of the products of local derivatives along the path.

## 4. Forward mode: dual numbers

Carry a derivative alongside every value: a **dual number** $a + b\varepsilon$ with the rule $\varepsilon^2 = 0$. Arithmetic does the chain rule automatically: $(a + b\varepsilon)(c + d\varepsilon) = ac + (ad + bc)\varepsilon$, and for any smooth $g$, $g(a + b\varepsilon) = g(a) + g'(a)\,b\,\varepsilon$. Seed the input with $x + 1\varepsilon$, run the program unchanged, and read the derivative off the $\varepsilon$ part: exact, with no step size.

::::derivation{id=d2 title="Dual-number arithmetic"}
:::step
$(3 + \varepsilon)^2 = 9 + 6\varepsilon + \varepsilon^2 = 9 + 6\varepsilon$. The derivative of $x^2$ at 3 is [[6]].
:::
:::step
$\sin\big((1 + \varepsilon)^2\big) = \sin(1 + 2\varepsilon) = \sin 1 + 2\cos(1)\,\varepsilon$. The derivative of $\sin(x^2)$ at 1 is [[2*cos(1)]].
:::
::::

One forward pass gives one JVP, the derivative along one input direction. A full gradient of $n$ inputs needs $n$ passes.

## 5. Reverse mode

Run the program forward, storing every node's value. Then give each node an **adjoint** $\bar v = \partial f / \partial v$: $\bar f = 1$ at the output, and, sweeping backward in reverse topological order,

$$
\bar v = \sum_{w \text{ uses } v} \bar w \, \frac{\partial w}{\partial v} .
$$

Each step is a VJP of one operation. When the sweep reaches the inputs, $\bar x_j = \partial f/\partial x_j$ for **every** input at once. The sum is essential: a value used in several places collects a contribution from each.

::::derivation{id=d3 title="A backward sweep by hand"}
:::step
$f = xy + \sin x$ at $(x, y) = (2, 3)$. With $a = xy$ and $b = \sin x$, $\bar f = 1$ gives $\bar a = \bar b = 1$. Then $\bar y = \bar a \cdot x =$ [[2]].
:::
:::step
$x$ is used twice, so $\bar x = \bar a \cdot y + \bar b \cdot \cos x =$ [[3 + cos(2)]].
:::
::::

::::predict{id=p3 kind=choice answer=b}
$y = x \cdot x$ is computed by one multiplication node whose two arguments are the same $x$. A reverse-mode engine sets each argument's adjoint to the upstream adjoint times the other argument. What must it do to get $dy/dx = 2x$?

- Nothing: it gets $2x$ automatically.
- Add the two contributions, $x$ and $x$, into the adjoint of $x$, rather than overwrite one with the other.
- Multiply the two contributions.
- Treat the node as a square and use $2x$ directly; the general rule cannot handle it.

:::reveal
Add them. Each use of $x$ contributes $\bar y \cdot x$; overwriting keeps only one and returns $x$, half the right answer. Every framework accumulates gradients with `+=` for this reason, which is also why stale gradients must be zeroed between steps.
:::
::::

## 6. The workhorse VJPs

- **Matmul** $Y = XW$: $\bar X = \bar Y W^\top$, $\bar W = X^\top \bar Y$.
- **Elementwise** $y = g(x)$: $\bar x = \bar y \odot g'(x)$.
- **Sum** $s = \sum_i x_i$: $\bar x_i = \bar s$, a broadcast; and broadcasting in the forward pass becomes a sum in the backward pass.
- **Log** $y = \log x$: $\bar x = \bar y / x$.
- **Softmax** $p = \operatorname{softmax}(z)$: $\bar z = p \odot (\bar p - \bar p \cdot p)$, from the Jacobian $\operatorname{diag}(p) - pp^\top$.

Composing the last two for the cross-entropy $L = -\log p_c$ gives the cleanest formula in deep learning: $\partial L/\partial z = p - y$, with $y$ the one-hot vector of the correct class $c$ (M27 derives it from information theory).

::::derivation{id=d4 title="Cross-entropy through the softmax"}
:::step
With $p = (0.5, 0.3, 0.2)$ and correct class 1, $\partial L/\partial z = p - y$, whose first entry is [[-0.5]].
:::
:::step
Its entries always add up to [[0]]: raising every logit by the same amount changes nothing.
:::
::::

## 7. The cost argument

A gradient is a product $u^\top J_K J_{K-1} \cdots J_1$ with $u = 1$ for a scalar output. Multiplied from the left, every partial product is a single row vector: $K$ VJPs, together a small constant times the cost of evaluating $f$. Multiplied from the right, each pass carries one input direction: $n$ passes for $n$ inputs. In general, forward mode costs one pass per input and reverse mode one pass per output.

::::derivation{id=d5 title="Counting passes"}
:::step
For $f: \mathbb{R}^{10^6} \to \mathbb{R}$, forward mode needs $10^6$ passes for the gradient and reverse mode needs [[1]].
:::
:::step
For $g: \mathbb{R} \to \mathbb{R}^{1000}$, the full Jacobian needs 1 forward pass but [[1000]] reverse passes.
:::
::::

Reverse mode pays in memory: every intermediate value used by a backward step must be stored or recomputed. Activation memory is the main constraint on training large models (L14), and checkpointing trades it for recomputation.

:::edge{to=L03 text="backpropagation is reverse mode applied to a network's layers."}
:::

:::edge{to=L04 text="an autograd engine for tensors, built from these VJPs."}
:::

:::edge{to=M26 text="automatic differentiation has no step size and no truncation error; finite differences have both."}
:::

:::edge{to=M27 text="the cross-entropy gradient p - y, derived from information theory."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Matrix derivative | perturb, keep first order, read the pairing | layer gradients |
| Matmul VJP | $\bar X = \bar Y W^\top$, $\bar W = X^\top \bar Y$ | every linear layer |
| JVP, VJP | $Jv$, $u^\top J$ without forming $J$ | cheap derivatives |
| Forward mode | dual numbers, $\varepsilon^2 = 0$ | one pass per input |
| Reverse mode | adjoints swept backward, summed over uses | one pass per output |
| Softmax and cross-entropy | $\partial L/\partial z = p - y$ | classification |
| Cost | gradient for a few evaluations; memory for intermediates | training at scale |
