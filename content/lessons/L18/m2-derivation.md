# Derivation: memory, communication and four ways to split a model

## 1. Memory accounting

Training a model with $\Psi$ parameters in mixed precision with Adam keeps:

- **weights** in 16-bit for the forward and backward passes: $2\Psi$ bytes;
- **gradients** in 16-bit: $2\Psi$;
- **optimizer states** in fp32: master weights, momentum and variance, $12\Psi$;
- **activations**: everything backward needs, which grows with batch, sequence length and depth.

The first three, $16\Psi$, are the **model states** (Rajbhandari et al., 2020).

:::edge{from=L17 text="bytes per parameter in mixed precision"}
:::

## 2. Activations, counted

Korthikanti et al. (2022) count the bytes one transformer layer stores for backward, in 16-bit, for sequence length $s$, micro-batch $b$, width $h$ and $a$ heads. The attention block keeps its input, $Q$ and $K$, $V$, the projection input and a dropout mask ($11sbh$), plus the $a$ attention matrices of size $s \times s$: scores after softmax, the dropout mask and the dropped-out scores ($5as^2b$). The MLP keeps its input, the $4h$-wide pre-activation and activation and a mask ($19sbh$), and the two layer norms their inputs ($4sbh$):
$$
\text{activations per layer} = s\,b\,h\left(34 + \frac{5\,a\,s}{h}\right) \text{ bytes}.
$$
FlashAttention (L12) never stores the $s \times s$ matrices, removing the second term.

::::derivation{id=d1 title="Activations of a large model"}
:::step
GPT-3 175B has $h = 12288$, $a = 96$, and is trained with $s = 2048$. For one sequence, $5as/h =$ [[80]].
:::
:::step
One layer stores $2048 \cdot 12288 \cdot 114 \approx$ [[2.87e9|tol=1e7]] bytes.
:::
:::step
Across 96 layers that is about [[275|tol=1]] GB, for a single sequence.
:::
::::

:::edge{from=L08 text="tensors saved for backward"}
:::

## 3. Collectives and what they cost

Distributed training moves data with a few **collectives** over $P$ ranks: **all-reduce** (every rank ends with the sum of everyone's arrays), **reduce-scatter** (every rank ends with the sum of one $1/P$ slice) and **all-gather** (every rank ends with every rank's slice).

A **ring** implementation arranges the ranks in a cycle and splits each array into $P$ chunks. Reduce-scatter takes $P - 1$ steps; in each, every rank passes one chunk to its neighbor, who adds it. All-gather passes the finished chunks around in another $P - 1$ steps. With $\alpha$ the latency of a step and $\beta$ the seconds per byte,
$$
T_\text{all-reduce} = 2(P-1)\,\alpha + 2\,\frac{P - 1}{P}\, n\, \beta.
$$
Each rank sends just under $2n$ bytes whatever $P$ is: the ring is bandwidth-optimal, and latency is what grows with $P$. Inside a server, GPUs talk over NVLink at hundreds of GB/s; between servers the network gives each GPU an order of magnitude less, which decides where each kind of parallelism goes.

::::derivation{id=d2 title="Ring traffic"}
:::step
All-reducing 1 GB over 8 GPUs, each GPU sends $2 \cdot \frac{7}{8} =$ [[1.75]] GB.
:::
:::step
Over 1024 GPUs it sends about [[2|tol=0.01]] GB.
:::
:::step
The fp16 gradients of a 7B model are 14 GB; over 64 GPUs each sends $2 \cdot \frac{63}{64} \cdot 14 \approx$ [[27.56|tol=0.02]] GB per step.
:::
::::

:::edge{from=L11 text="bandwidth, latency and overlapping work"}
:::

## 4. Data parallelism

Every GPU holds the whole model and a different slice of the batch. After backward, an all-reduce averages the gradients, and every GPU applies the same update, so the copies never diverge. PyTorch's DDP groups gradients into buckets and starts each bucket's all-reduce as soon as backward has produced it, overlapping communication with the rest of the backward pass. Data parallelism scales the batch, not the model: memory per GPU stays $16\Psi$ plus activations.

## 5. ZeRO: sharding the model states

Data-parallel ranks hold identical model states, which is wasteful. **ZeRO** (Rajbhandari et al., 2020) shards them over the $N_d$ data-parallel ranks:

- **stage 1** shards the optimizer states: each rank updates its $1/N_d$ of the parameters, $(2 + 2 + 12/N_d)\Psi$ bytes;
- **stage 2** also shards the gradients: a reduce-scatter leaves each rank only the gradients it updates, $(2 + 14/N_d)\Psi$;
- **stage 3** also shards the weights, all-gathered layer by layer when needed (PyTorch's FSDP), $16\Psi/N_d$.

Stages 1 and 2 communicate exactly what data parallelism does (a reduce-scatter and an all-gather make an all-reduce); stage 3 adds an all-gather of the weights in backward, 1.5 times the traffic.

::::derivation{id=d3 title="ZeRO for 7.5B parameters on 64 GPUs"}
:::step
Without sharding: $16 \cdot 7.5 =$ [[120]] GB per GPU.
:::
:::step
Stage 1: $(4 + 12/64) \cdot 7.5 \approx$ [[31.4|tol=0.1]] GB.
:::
:::step
Stage 3: $16 \cdot 7.5 / 64 \approx$ [[1.875|tol=0.001]] GB.
:::
::::

## 6. Tensor parallelism

Split the matrices themselves (Shoeybi et al., 2019). In the MLP, split the first weight by **columns**: each of $t$ GPUs computes a slice of the hidden units, and the elementwise activation needs no communication. Split the second by **rows**: each GPU multiplies its hidden slice by its rows, producing a partial output, and **one all-reduce** sums them. Attention splits the same way by heads: the $Q, K, V$ projections by columns (whole heads per GPU), the output projection by rows. Each layer costs two all-reduces of the $s \times b \times h$ activations in forward and two in backward, inside every layer, so tensor parallelism needs the fast links within a server and is usually limited to 8 GPUs. **Sequence parallelism** additionally splits the layer norms and dropout along the sequence, dividing all of the activations by $t$.

## 7. Pipeline parallelism

Give each of $p$ stages a contiguous block of layers, and stream $m$ **micro-batches** through: stage $s$ starts on micro-batch $j$ as soon as stage $s-1$ is done with it. While the pipeline fills and drains, stages sit idle: with every micro-batch taking $t_f + t_b$ per stage, a step takes $(m + p - 1)(t_f + t_b)$ instead of $m(t_f + t_b)$, a **bubble** of
$$
\frac{p - 1}{m + p - 1}
$$
of the time. **GPipe** runs all forwards, then all backwards, holding $m$ micro-batches' activations; **1F1B** alternates one forward and one backward once the pipeline is full, holding at most $p$. Pipeline stages exchange only the activations at their boundary, so pipelines can span servers.

::::derivation{id=d4 title="The bubble"}
:::step
With 4 stages and 4 micro-batches, the bubble is $3/7 \approx$ [[0.4286|tol=0.0005]] of the step.
:::
:::step
With 32 micro-batches it falls to $3/35 \approx$ [[0.0857|tol=0.0005]].
:::
::::

## 8. Activation checkpointing

Keep only some activations (typically each layer's input) and recompute the rest during backward. Memory for activations drops from all of them to one input per layer plus one layer's worth; the price is one extra forward pass, about a third more compute. Applied to every $k$-th of $L$ layers, storage is about $L/k + k$ activations, smallest at $k = \sqrt{L}$ (Chen et al., 2016).

## 9. Putting it together

Large runs combine all of these, "3D parallelism": tensor parallelism inside a server, pipeline stages across servers, data parallelism (often with ZeRO stage 1) over the replicas, and checkpointing where activations still do not fit. The planner follows the same order of preference: model parallelism adds communication inside every layer, so use as little of it as the memory allows.

:::edge{from=L15 text="compute-optimal model sizes"}
:::

:::edge{to=L19 text="A real pretraining run, data parallel and resumable."}
:::
