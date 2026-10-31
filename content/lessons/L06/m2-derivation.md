# Derivation: normalization layers and residual streams

## 1. Batch normalization

For a minibatch $X$ of shape $N \times d$, **batch norm** normalizes each feature (column) with the batch's own statistics:

$$
\mu_j = \frac1N \sum_i x_{ij}, \qquad \sigma_j^2 = \frac1N \sum_i (x_{ij} - \mu_j)^2, \qquad \hat x_{ij} = \frac{x_{ij} - \mu_j}{\sqrt{\sigma_j^2 + \epsilon}}, \qquad y_{ij} = \gamma_j \hat x_{ij} + \beta_j.
$$

The learned $\gamma$ and $\beta$ let the layer undo the normalization if that helps. At evaluation time there may be one example, so batch norm keeps **running averages** of $\mu$ and $\sigma^2$ during training and uses those instead. The output of an example in training mode therefore depends on the other examples in its batch.

## 2. Its backward pass

Write $r = 1/\sqrt{\sigma^2 + \epsilon}$ and $g = \partial L/\partial \hat x = \gamma \odot \partial L/\partial y$, per feature. Every $x_i$ affects $\hat x_i$ directly, and every $\hat x_k$ through $\mu$ and $\sigma^2$. Collecting the three paths and using $\sum_i \hat x_i = 0$ and $\sum_i \hat x_i^2 = N$ (up to $\epsilon$):

$$
\frac{\partial L}{\partial x_i} = \frac{r}{N}\left(N g_i - \sum_k g_k - \hat x_i \sum_k g_k \hat x_k\right).
$$

The two subtracted terms remove the components of $g$ along the directions the normalization cannot see: a constant shift of the batch and a rescaling of it.

::::derivation{id=d1 title="What batch norm's gradient removes"}
:::step
Over a batch of $N = 4$, the normalized values of one feature sum to [[0]] and their squares sum to [[4]].
:::
:::step
If the upstream gradient is the same for every example, $g = (1, 1, 1, 1)$, the formula gives $\partial L/\partial x_i =$ [[0]] for every $i$: shifting the whole batch does not change the output.
:::
:::step
If $g = 3\hat x$, the three terms are $3N\hat x_i$, $0$ and $\hat x_i \cdot 3N$, so the gradient is again [[0]]: scaling the batch does not change the output either.
:::
::::

## 3. Layer norm and RMSNorm

**Layer norm** applies the same formulas to each example (row) over its $d$ features, with per-feature $\gamma, \beta$. No batch statistics are involved, so training and evaluation agree and a batch of one works. Its backward pass is the batch-norm formula with sums over features instead of over the batch, which is why transformers, with variable-length sequences and small per-device batches, use it.

**RMSNorm** drops the centering: $y = \gamma \odot x / \operatorname{rms}(x)$ with $\operatorname{rms}(x) = \sqrt{\tfrac1d\sum_j x_j^2 + \epsilon}$. With $r = \operatorname{rms}(x)$ and $g = \gamma \odot \partial L/\partial y$,

$$
\frac{\partial L}{\partial x_j} = \frac{g_j}{r} - \frac{x_j}{d\, r^3}\sum_k g_k x_k.
$$

It is cheaper (one reduction instead of two) and works as well in practice; LLaMA-style models use it.

::::derivation{id=d2 title="RMSNorm by hand"}
:::step
For $x = (3, 4)$, $d = 2$ and $\epsilon$ negligible, $\operatorname{rms}(x) = \sqrt{12.5} \approx$ [[3.5355|tol=0.001]].
:::
:::step
With $\gamma = (1, 1)$, the first output is $3/3.5355 \approx$ [[0.8485|tol=0.001]]. The output's root mean square is exactly [[1]].
:::
::::

## 4. Residual connections

A **residual block** computes $h_{l+1} = h_l + F_l(h_l)$. Its Jacobian is $I + J_{F_l}$, so the gradient reaching layer 0 is

$$
\frac{\partial L}{\partial h_0} = \frac{\partial L}{\partial h_L} \prod_{l} (I + J_{F_l}),
$$

and expanding the product gives one term that is the identity: a path along which the gradient arrives unchanged, however many layers there are. In a plain stack every path is a product of $L$ Jacobians, which shrinks or grows geometrically.

The forward pass pays for it. If each branch output has zero mean, is uncorrelated with $h_l$, and has second moment $\alpha^2 \mathbb E[h_l^2]$, then $\mathbb E[h_{l+1}^2] = (1 + \alpha^2)\,\mathbb E[h_l^2]$, and the stream grows geometrically with depth.

::::derivation{id=d3 title="Growth of the residual stream"}
:::step
With $\alpha = 1$, the root mean square after 20 layers has grown by $2^{10} =$ [[1024]].
:::
:::step
Scaling every branch by $\alpha = 1/\sqrt L$ gives $(1 + 1/L)^{L/2}$, which tends to $\sqrt e \approx$ [[1.6487|tol=0.001]] as $L$ grows: bounded at any depth.
:::
::::

One caution, which exercise 5 measures: a branch that ends in a ReLU has a positive mean, so its outputs are correlated across layers and the stream grows faster than the formula. Real residual branches end in a linear layer, whose output has zero mean, and then the formula holds.

## 5. Pre-norm and post-norm

There are two ways to combine normalization with a residual connection:

- **Post-norm** (the original transformer): $h_{l+1} = \operatorname{LN}(h_l + F(h_l))$. The stream is renormalized after every block, so even the skip path passes through $L$ normalizations, each with its own Jacobian. Gradients at initialization are uneven across depth, and large early updates can push the network into a bad region; post-norm transformers need learning-rate warmup (Xiong et al., 2020).
- **Pre-norm** (GPT-2 onward): $h_{l+1} = h_l + F(\operatorname{LN}(h_l))$. Only the branch input is normalized, so the skip path is a clean sum from any layer to the output. The stream's scale grows slowly with depth, so a final layer norm is applied before the output layer.

::::derivation{id=d4 title="The pre-norm stream"}
:::step
Each of 30 pre-norm blocks adds an update of root mean square 1, uncorrelated with the stream, to a stream that starts with root mean square 1. The final root mean square is about $\sqrt{31} \approx$ [[5.568|tol=0.01]].
:::
:::step
In post-norm, the stream after every block has root mean square [[1]] (with $\gamma = 1$, $\beta = 0$), whatever the depth.
:::
::::

:::edge{to=L09 text="Every transformer block is a pre-norm residual block, twice: x + attention(LN(x)), then x + MLP(LN(x))."}
:::

:::edge{to=L08 text="The layer norm forward and backward become one fused GPU kernel."}
:::

:::edge{from=L05 text="variance-preserving initialization, Adam and warmup"}
:::

## Summary

| Layer | Normalizes over | Train and eval differ | Batch of one |
| --- | --- | --- | --- |
| Batch norm | the batch, per feature | yes (running statistics) | fails |
| Layer norm | the features, per example | no | works |
| RMSNorm | the features, no centering | no | works |

| Block | Formula | Skip path |
| --- | --- | --- |
| Plain | $F(h)$ | none |
| Residual | $h + F(h)$ | identity, but the stream grows |
| Post-norm | $\operatorname{LN}(h + F(h))$ | through every norm; needs warmup |
| Pre-norm | $h + F(\operatorname{LN}(h))$ | identity; final norm before the output |
