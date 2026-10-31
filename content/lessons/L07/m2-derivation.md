# Derivation: the multi-layer perceptron and its backward pass

You will write down a multi-layer perceptron (MLP), see why it can represent far more than a linear model, derive the backward pass of every layer it uses, assemble them into backpropagation, count the cost, and look at the training loop and the ways initialization can make it fail before it starts.

## 1. The forward pass

An MLP with two hidden layers maps a batch $X \in \mathbb{R}^{B \times d}$ to logits:

$$
\begin{aligned}
Z_1 &= XW_1 + \mathbf 1 b_1^\top, & H_1 &= \phi(Z_1), \\
Z_2 &= H_1W_2 + \mathbf 1 b_2^\top, & H_2 &= \phi(Z_2), \\
Z_3 &= H_2W_3 + \mathbf 1 b_3^\top, & L &= \operatorname{CE}\big(\operatorname{softmax}(Z_3), y\big).
\end{aligned}
$$

$\phi$ is applied elementwise: $\operatorname{ReLU}(z) = \max(0, z)$ or $\tanh(z)$. Without $\phi$ the composition would collapse into a single linear map, $X(W_1W_2W_3)$, no more expressive than L05's model. The nonlinearity is what lets layers build new features.

::::derivation{id=d1 title="Counting parameters"}
:::step
Layer sizes $64 \to 64 \to 32 \to 10$. The first layer has $64 \times 64$ weights and $64$ biases: [[4160]] parameters.
:::
:::step
The whole network has $4160 + (64 \cdot 32 + 32) + (32 \cdot 10 + 10) =$ [[6570]] parameters.
:::
:::step
Remove both nonlinearities and the network computes $X W_1 W_2 W_3$ plus a bias: a linear map from 64 inputs to 10 logits, which needs only $64 \cdot 10 + 10 =$ [[650]] parameters to represent.
:::
::::

## 2. Why one hidden layer can approximate anything

In one dimension, a hidden ReLU unit $\max(0, w x + b)$ is a hinge: flat on one side of $x = -b/w$, linear on the other. A sum of $k$ hinges plus a bias is a **piecewise linear** function with at most $k$ kinks, so at most $k + 1$ linear pieces. Placing kinks at chosen points and choosing the output weights as slope changes reproduces any piecewise linear interpolation of a target function.

::::derivation{id=d2 title="Building a function out of hinges"}
:::step
To interpolate a curve at knots $t_0 < t_1 < \dots < t_k$ with slopes $m_1, \dots, m_k$ on the pieces between them, start with value $f(t_0)$ and slope $m_1$, then add a hinge $\max(0, x - t_j)$ at each interior knot $t_j$ with output weight equal to the change in slope, $m_{j+1} - m_j$. If the slope goes from $2$ to $-1$ at $t_1$, that weight is [[-3]].
:::
:::step
With knots spaced $h$ apart, linear interpolation of a smooth $f$ has error at most $\tfrac18 h^2 \max|f''|$. For $f(x) = \sin(\pi x)$ on $[-1, 1]$ with 20 equal pieces ($h = 0.1$), the bound is $\tfrac18 \cdot 0.01 \cdot \pi^2 \approx$ [[0.01234]].
:::
:::step
Halving $h$ divides that error bound by [[4]], so accuracy improves steadily with width. The **universal approximation theorem** says the same holds in any dimension and for any non-polynomial activation: a wide enough single hidden layer approximates any continuous function on a bounded region. It says nothing about how many units are needed or whether gradient descent finds them, which is why depth and good training matter in practice.
:::
::::

## 3. The backward pass of each layer

Reverse mode (M19) needs, for each layer, the map from the gradient at its output to the gradients at its input and its parameters. Write $G = \partial L/\partial(\text{output})$.

**Linear layer** $Y = XW + \mathbf 1 b^\top$:

$$
\frac{\partial L}{\partial X} = G W^\top, \qquad \frac{\partial L}{\partial W} = X^\top G, \qquad \frac{\partial L}{\partial b} = G^\top \mathbf 1 .
$$

The bias gradient sums $G$ over the batch because $b$ is added to every row.

**Elementwise activation** $Y = \phi(Z)$: the Jacobian is diagonal, so $\partial L/\partial Z = G \odot \phi'(Z)$. For ReLU, $\phi'(z) = [z > 0]$: the gradient passes where the unit was active and is blocked where it was not. For $\tanh$, $\phi'(z) = 1 - \tanh^2(z) = 1 - Y^2$, conveniently computed from the saved output.

**Softmax cross-entropy**, averaged over a batch of $B$ examples: $\partial L/\partial Z_3 = (P - Y_{\text{onehot}})/B$ (M27).

::::derivation{id=d3 title="Shapes and values in a backward pass"}
:::step
With a batch of $B = 32$, hidden width 64 and 10 classes, the output-layer gradient $\partial L/\partial Z_3$ has shape $32 \times 10$, and $\partial L/\partial W_3 = H_2^\top\,\partial L/\partial Z_3$ has as many rows as $H_2$ has columns. For $H_2$ of width 32, that is [[32]] rows.
:::
:::step
A ReLU unit with pre-activation $z = -0.4$ receives upstream gradient $g = 1.5$. The gradient passed to $z$ is [[0]].
:::
:::step
A tanh unit with output $y = 0.8$ receives upstream gradient $g = 2$. The gradient passed to its input is $2(1 - 0.64) =$ [[0.72]].
:::
:::step
The bias gradient of a layer is the sum of $G$ over the batch. If the four rows of a one-column $G$ are $0.1, -0.2, 0.3, 0.05$, it equals [[0.25]].
:::
::::

## 4. Backpropagation

Chain the layer VJPs from the loss back to the input:

1. Forward pass: compute and **save** $X, Z_1, H_1, Z_2, H_2, Z_3$.
2. $G_3 = (P - Y)/B$; then $\nabla W_3 = H_2^\top G_3$, $\nabla b_3 = G_3^\top\mathbf 1$.
3. $G_2 = (G_3 W_3^\top) \odot \phi'(Z_2)$; then $\nabla W_2 = H_1^\top G_2$, $\nabla b_2 = G_2^\top\mathbf 1$.
4. $G_1 = (G_2 W_2^\top) \odot \phi'(Z_1)$; then $\nabla W_1 = X^\top G_1$, $\nabla b_1 = G_1^\top \mathbf 1$.

That is all of backpropagation for an MLP: one rule per layer type, applied in reverse order, using activations saved from the forward pass. Every gradient can and must be checked with central differences (M15, M18), one layer at a time.

:::edge{from=M19 text="vector-Jacobian products and the matmul VJP"}
:::

:::edge{from=L05 text="softmax regression and its gradient"}
:::

## 5. What it costs

A linear layer's forward pass is one matrix product: about $2 B n_{\text{in}} n_{\text{out}}$ floating-point operations. Its backward pass is two: $GW^\top$ and $X^\top G$. Elementwise layers are negligible.

::::derivation{id=d4 title="The cost ratio"}
:::step
A layer with $B = 128$, $n_{\text{in}} = 512$ and $n_{\text{out}} = 512$ costs $2 \cdot 128 \cdot 512 \cdot 512 \approx$ [[67108864]] FLOPs forward.
:::
:::step
The backward pass costs [[2]] times as much as the forward pass for that layer (the first layer can skip $\partial L/\partial X$ and costs only one product).
:::
:::step
So one training step costs about $1 + 2 = 3$ forward passes. The forward pass for one token of a model with $N$ parameters costs about $2N$ FLOPs, so a training step costs about [[6]] FLOPs per parameter per token. This is the $C \approx 6ND$ rule of L15.
:::
::::

Memory is the other cost: every saved activation must stay alive until the backward pass reaches it. For an MLP that is $B \times (\text{sum of layer widths})$ numbers; for a large transformer it dominates training memory (L18).

## 6. Training: minibatch stochastic gradient descent

The full-data gradient averages over all $n$ examples. A **minibatch** of $B$ randomly chosen examples gives an unbiased estimate whose variance shrinks like $1/B$, at a cost proportional to $B$. Training loops repeat: shuffle, split into batches, and for each batch run forward, backward and an update $\theta \leftarrow \theta - \eta \nabla_\theta L$. One pass through the data is an **epoch**.

::::derivation{id=d5 title="Minibatch noise"}
:::step
If one example's gradient has variance $v$ (per coordinate) and examples are sampled independently, a minibatch average of $B$ of them has variance [[v/B]].
:::
:::step
Going from batch size 32 to 128 cuts the standard deviation of the gradient estimate by a factor of [[2]], at four times the compute per step.
:::
::::

## 7. Initialization: three ways to fail before training starts

**Symmetry.** If all weights in a layer start equal, all its units compute the same function and receive identical gradients, so they remain equal forever. Initialize weights randomly; biases can start at zero.

**Dead units.** A ReLU unit whose pre-activation is negative on every input outputs zero and receives zero gradient: it never recovers. Large negative biases or a huge learning-rate step that pushes weights into that region kill units permanently.

**Exploding or vanishing activations.** Each layer multiplies the scale of its input by roughly $\sqrt{n_{\text{in}}}$ times the standard deviation of its weights (with a factor $1/\sqrt2$ for ReLU, which zeroes half its inputs). Over many layers the scale grows or shrinks geometrically.

::::derivation{id=d6 title="Activation scale through depth"}
:::step
For ReLU layers of width $n$ with weights of standard deviation $s$, the root mean square of the activations is multiplied by about $s\sqrt{n/2}$ per layer. With $n = 256$ and $s = 1$, that factor is $\sqrt{128} \approx$ [[11.31]].
:::
:::step
After 10 such layers the activations are larger by about $128^{5} \approx 3.4 \times 10^{10}$. Choosing $s = \sqrt{2/n}$ makes the factor exactly [[1]]: this is He initialization, derived properly in L09.
:::
::::

:::widget{name=ActivationStats depth=10 init=unit act=relu}
:::

Switch the initialization in the widget between $\mathcal N(0, 1)$, Xavier and He and watch the activation scale across layers.

:::edge{to=L09 text="Xavier and He initialization derived from variance preservation; momentum, Adam and schedules."}
:::

:::edge{to=L21 text="The output-layer gradient p - onehot(y) returns as the score function in policy gradients."}
:::

## Summary

| Layer | Forward | Backward to input | Backward to parameters |
| --- | --- | --- | --- |
| Linear | $XW + b$ | $GW^\top$ | $X^\top G$, $\sum_{\text{batch}} G$ |
| ReLU | $\max(0, Z)$ | $G \odot [Z > 0]$ | none |
| tanh | $\tanh Z$ | $G \odot (1 - Y^2)$ | none |
| Softmax CE | $-\log p_y$ | $(P - Y)/B$ | none |
