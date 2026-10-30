# Derivation: attention, heads, positions and the transformer block

## 1. Attention as a soft lookup

Stack a sequence of $n$ vectors as the rows of $X$ ($n \times d$). Three learned projections give **queries** $Q = XW_Q$, **keys** $K = XW_K$ and **values** $V = XW_V$. The scores, weights and output are
$$
S = \frac{QK^\top}{\sqrt{d_k}}, \qquad P = \operatorname{softmax}_{\text{rows}}(S), \qquad O = PV.
$$
Row $i$ of $O$ is a weighted average of the values, with weights from how well query $i$ matches every key.

:::edge{from=M10 text="dot products as similarity and matrix products"}
:::

:::edge{from=L05 text="the softmax and its Jacobian"}
:::

## 2. Why divide by the square root of the dimension

If the entries of $q$ and $k$ are independent with mean 0 and variance 1, then $q \cdot k = \sum_{j=1}^{d} q_j k_j$ has mean 0 and variance $d$.

::::derivation{id=d1 title="The scale of a dot product"}
:::step
For $d_k = 64$, the score $q \cdot k$ has variance [[64]] and standard deviation [[8]].
:::
:::step
After dividing by $\sqrt{64}$, its variance is [[1]], whatever the dimension.
:::
::::

Why it matters: the softmax's Jacobian is $\operatorname{diag}(p) - pp^\top$. When one weight approaches 1, every entry of that matrix approaches 0, and so does the gradient reaching the scores.

::::derivation{id=d2 title="A saturated softmax"}
:::step
For two scores $(0, 8)$, the softmax puts weight $e^8/(1 + e^8) \approx$ [[0.99966|tol=0.00002]] on the second.
:::
:::step
The derivative of that weight with respect to its own score is $p(1 - p) \approx$ [[0.000335|tol=0.00001]], against 0.25 when the two scores are equal.
:::
::::

## 3. The causal mask

A language model predicts token $t + 1$ from tokens $1, \dots, t$. Set the scores of every key after the query to $-\infty$ before the softmax: those weights become exactly 0, and position $i$ sees only positions $1, \dots, i$. Because no position sees its own future, one forward pass over a sequence of $n$ tokens yields $n$ valid next-token predictions, all trained at once.

## 4. Multiple heads

One softmax can only form one weighted average per position. **Multi-head attention** splits the $d$ dimensions into $h$ heads of $d/h$ dimensions, runs attention independently in each, concatenates the $h$ outputs and mixes them with an output projection $W_O$. Each head can attend to a different position for a different reason (one to the previous token, another to the subject of the sentence) at the same cost as a single head of width $d$.

::::derivation{id=d3 title="Counting"}
:::step
With a causal mask over $n = 6$ positions, the number of query-key pairs that are not masked is $n(n + 1)/2 =$ [[21]].
:::
:::step
A model of width $d = 512$ with $h = 8$ heads gives each head [[64]] dimensions.
:::
::::

## 5. Positions

Attention treats its input as a set. Permute the rows of $X$ and, without a mask, the rows of the output are permuted the same way: attention is **permutation-equivariant**. Word order has to be supplied.

**Sinusoidal encodings** add to the input a vector $\text{PE}_{p}$ with $\text{PE}_{p, 2i} = \sin(p\,\omega_i)$ and $\text{PE}_{p, 2i+1} = \cos(p\,\omega_i)$, with frequencies $\omega_i = 10000^{-2i/d}$. Learned position embeddings (used in the capstone) are a table of trainable vectors instead.

**Rotary embeddings** (RoPE) rotate each pair of query and key coordinates $(2i, 2i + 1)$ by the angle $p\,\theta_i$. Rotations compose: $R(m\theta)^\top R(n\theta) = R((n - m)\theta)$, so
$$
\big(R(m\theta)\,q\big)^\top \big(R(n\theta)\,k\big) = q^\top R((n - m)\theta)\, k,
$$
and the score depends only on the **relative** position $n - m$.

::::derivation{id=d4 title="Positions"}
:::step
At position 0, the sinusoidal encoding's even coordinates are all [[0]] and its odd coordinates are all [[1]].
:::
:::step
With $\theta = 0.1$, a query at position 3 and a key at position 7 interact through a rotation by [[0.4]] radians.
:::
::::

## 6. The backward pass of attention

With $c = 1/\sqrt{d_k}$, $O = PV$, $P = \operatorname{softmax}(S)$ and $S = cQK^\top$, and $\partial L/\partial O = \text{d}O$:
$$
\begin{aligned}
\text{d}V &= P^\top \text{d}O, \qquad \text{d}P = \text{d}O\, V^\top, \\
\text{d}S &= P \odot \big(\text{d}P - \operatorname{rowsum}(\text{d}P \odot P)\big), \\
\text{d}Q &= c\,\text{d}S\, K, \qquad \text{d}K = c\,\text{d}S^\top Q.
\end{aligned}
$$
The middle formula is L05's softmax Jacobian applied row by row.

::::derivation{id=d5 title="One query, two positions"}
:::step
A query attends to two positions with weights $P = (0.25, 0.75)$ and scalar values $v = (2, 6)$. Its output is [[5]].
:::
:::step
With $\text{d}O = 1$, the gradient reaching the second value is [[0.75]].
:::
:::step
$\text{d}P = (2, 6)$, and $\text{d}S = P \odot (\text{d}P - 5)$, so the gradient of the first score is [[-0.75]]: raising it would move weight toward the smaller value.
:::
::::

:::edge{from=L07 text="backpropagation through matrix products"}
:::

## 7. The decoder block

A transformer decoder stacks $L$ identical **pre-norm residual blocks** (L10), each with two branches:
$$
x \leftarrow x + \operatorname{MHA}(\operatorname{LN}_1(x)), \qquad x \leftarrow x + \operatorname{MLP}(\operatorname{LN}_2(x)),
$$
where the MLP maps $d \to 4d \to d$ with a GELU. Attention moves information between positions; the MLP processes each position on its own. Token and position embeddings feed the first block; a final layer norm and a linear layer to vocabulary logits follow the last.

**Parameters.** Attention has four $d \times d$ matrices ($4d^2$), the MLP two $d \times 4d$ matrices ($8d^2$): about $12d^2$ per block. **FLOPs.** About 2 per parameter per token in the forward pass, plus the attention itself: scores and weighted values cost $2nd$ each per layer, per token, for context length $n$.

::::derivation{id=d6 title="Sizes"}
:::step
At $d = 768$ (GPT-2 small), one block has about $12 \cdot 768^2 =$ [[7077888]] parameters.
:::
:::step
The attention term $4nd$ per layer equals the weight term $24d^2$ when the context length is $n = 6d$: for $d = 768$, [[4608]] tokens.
:::
::::

:::edge{from=L10 text="pre-norm residual blocks"}
:::

## 8. Attention on the roofline

The score matrix has $n^2$ entries per head. Computing it, applying the mask and softmax, and multiplying by $V$ in separate steps writes and reads that matrix through device memory several times, and the softmax in between is memory-bound. For long contexts this, not the FLOPs, is what makes naive attention slow, which is the problem FlashAttention solves in L12.

:::edge{from=L11 text="arithmetic intensity and the roofline"}
:::

:::edge{to=L12 text="Fuse scores, mask, softmax and weighted sum into one kernel: FlashAttention."}
:::

:::edge{to=L22 text="At inference, cache past keys and values instead of recomputing them."}
:::
