# Derivation: Triton kernels, fusion and FlashAttention

## 1. The Triton programming model

CUDA programs describe what one thread does. **Triton** programs describe what one **program instance** does to a block of data: you launch a grid of program instances, each finds its block with `tl.program_id`, builds vectors of offsets with `tl.arange`, loads whole blocks with `tl.load`, computes on them (`tl.dot` for small matrix products, reductions such as `tl.max` and `tl.sum`), and stores with `tl.store`. The compiler decides how the block is spread over threads, warps, registers and shared memory. Masks on loads and stores handle the ragged last block.

## 2. Coalesced access

A warp's 32 threads issue their loads together. If they read 32 consecutive 4-byte words, the hardware serves them with a few 32-byte transactions; if each thread reads an element far from its neighbour's, every thread needs its own transaction.

::::derivation{id=d1 title="Transactions per warp"}
:::step
32 threads reading consecutive fp32 values touch $128$ bytes: [[4]] aligned 32-byte segments.
:::
:::step
With a stride of 8 elements between threads, the warp touches [[32]] segments, and only $128/(32 \cdot 32) =$ [[0.125]] of the transferred bytes are used.
:::
::::

In row-major storage, reading along a row is coalesced and reading down a column is strided: lay out tiles so that consecutive threads read consecutive addresses.

## 3. Fusion

Written as separate operations, a row softmax reads its input for the maximum, reads it again and writes the exponentials, reads those for the sum, and reads them again to write the result: six arrays of traffic. A fused kernel keeps the row on chip: one read and one write.

::::derivation{id=d2 title="A fused softmax"}
:::step
For a $4096 \times 4096$ fp16 matrix, the unfused softmax moves $6 \cdot 4096^2 \cdot 2 =$ [[201326592]] bytes and the fused one [[67108864]].
:::
:::step
At 320 GB/s the fused kernel needs at least [[0.21|tol=0.01]] ms.
:::
::::

On the roofline, fusion does not move a kernel's arithmetic: it divides its bytes, which moves a memory-bound kernel to the right, to a higher intensity and a higher attainable throughput. The widget draws the softmax already fused, at 1.25 FLOP per byte in fp16; unfused, its six passes over memory would put it at about 0.42, three times further down the memory roof.

:::widget{name=Roofline hardware=t4 precision=fp16}
:::

:::edge{from=L07 text="the roofline, tiling and kernel fusion"}
:::

:::edge{from=L06 text="the layer norm forward and backward passes"}
:::

## 4. The online softmax

Process a vector in blocks. Keep $m$, the maximum so far, and $l = \sum_{\text{seen}} e^{x_j - m}$. For a new block $b$ with maximum $m_b$:
$$
m' = \max(m, m_b), \qquad l' = l\, e^{m - m'} + \sum_{j \in b} e^{x_j - m'}.
$$
Starting from $m = -\infty$, $l = 0$, after the last block $p_j = e^{x_j - m}/l$. Two summaries of disjoint parts merge the same way: $m = \max(m_1, m_2)$, $l = l_1 e^{m_1 - m} + l_2 e^{m_2 - m}$.

::::derivation{id=d3 title="Two blocks"}
:::step
The first block is $(1, 3)$: $m = 3$ and $l = e^{-2} + e^0 \approx$ [[1.1353|tol=0.0005]].
:::
:::step
The second block is $(2, 5)$: $m' = 5$, and $l' = 1.1353\, e^{-2} + e^{-3} + e^{0} \approx$ [[1.2034|tol=0.0005]], which equals $\sum_j e^{x_j - 5}$ over all four values.
:::
::::

## 5. FlashAttention

Apply the online softmax to attention. A program owns a block of queries $Q_i$ and keeps, per query, a running maximum $m$, a running sum $l$ and an accumulator $a$ for the output. For each block of keys and values $K_j, V_j$:
$$
S = c\,Q_i K_j^\top, \quad m' = \max(m, \operatorname{rowmax} S), \quad P = e^{S - m'}, \quad \alpha = e^{m - m'}, \quad l' = \alpha l + \operatorname{rowsum} P, \quad a' = \alpha a + P V_j.
$$
At the end, $O_i = a / l$. The $N \times N$ scores exist only one tile at a time, on chip. Standard attention moves $\Theta(Nd + N^2)$ elements to and from device memory; FlashAttention moves $\Theta(N^2 d^2 / M)$ for on-chip memory of $M$ elements, many times less for typical $d$ and $M$ (Dao et al., 2022).

For the backward pass, FlashAttention stores only $L_i = m + \ln l$, the log-sum-exp of each row, and recomputes each tile of probabilities as $P = e^{S - L}$. With $D_i = \sum_k \text{d}O_{ik} O_{ik}$, the softmax gradient becomes $\text{d}S = P \odot (\text{d}P - D)$: L09's formula, without the stored matrix.

::::derivation{id=d4 title="Memory for one head"}
:::step
At $N = 4096$, the attention weights of one head in fp16 take $4096^2 \cdot 2 =$ [[33554432]] bytes.
:::
:::step
FlashAttention keeps one fp32 log-sum-exp per query: [[16384]] bytes.
:::
::::

:::edge{from=L09 text="scaled dot-product attention and its backward pass"}
:::

## 6. Choosing block sizes

Each program holds its tiles in shared memory and registers. With block sizes $B_m$ (queries) and $B_n$ (keys) and head dimension $d$, a FlashAttention program needs a $B_m \times d$ query tile, $B_n \times d$ key and value tiles, and fp32 accumulators of $B_m \times d$ and $B_m \times B_n$. Larger blocks reuse each loaded value more; blocks too large for on-chip memory spill or fail to compile, and fewer programs fit on each SM.

::::derivation{id=d5 title="Fitting 64 KB"}
:::step
For $B_m = B_n = 64$ and $d = 64$: $(64 \cdot 64 + 2 \cdot 64 \cdot 64) \cdot 2 + 4 \cdot (64 \cdot 64 + 64 \cdot 64) =$ [[57344]] bytes, which fits in a T4 SM's 64 KB.
:::
::::

## 7. Numerics inside kernels

Load fp16, compute in fp32: $e^x$ overflows fp16 above $\ln 65504 \approx 11.09$, and an fp16 sum of thousands of terms loses its low bits. Subtract the maximum before exponentiating. For statistics such as a variance, the one-pass formula $\mathbb E[x^2] - \mathbb E[x]^2$ cancels catastrophically when the mean is large compared with the spread; Welford's update, $\delta = x - \mu$, $\mu \mathrel{+}= \delta / n$, $M_2 \mathrel{+}= \delta (x - \mu)$, does not.

:::edge{to=L18 text="Inference kernels: attention over cached and paged keys and values."}
:::
