# Derivation: GPUs, memory and the roofline

## 1. How a GPU executes a kernel

A GPU is many simple processors. The T4 has 40 **streaming multiprocessors** (SMs), each with 64 fp32 cores and 8 tensor cores. A kernel launch creates a grid of **thread blocks**; each block runs on one SM, and its threads execute in groups of 32 called **warps**, which issue the same instruction together. An SM holds many warps at once (up to 32 on the T4) and switches between them every cycle, so while one warp waits for memory, another computes. Keeping many warps resident, high **occupancy**, is how a GPU hides memory latency.

::::derivation{id=d1 title="Peak throughput"}
:::step
A warp has [[32]] threads. An SM with 32 resident warps therefore runs 1024 threads at once, and the whole T4 [[40960]].
:::
:::step
Peak fp32 throughput is SMs times cores per SM times clock times 2 FLOPs per fused multiply-add: $40 \cdot 64 \cdot 1.59 \times 10^9 \cdot 2 \approx$ [[8.14|tol=0.05]] TFLOP/s.
:::
::::

## 2. The memory hierarchy

Data lives at several levels, each smaller and faster than the next:

| Level | T4 size | Shared by |
| --- | --- | --- |
| Registers | 64K 32-bit registers per SM | one thread |
| Shared memory and L1 | up to 64 KB of shared memory per SM | one thread block |
| L2 cache | 4 MB | the whole GPU |
| Device memory (GDDR6) | 16 GB at 320 GB/s | the whole GPU |
| Host memory over PCIe 3.0 x16 | the machine's RAM, about 16 GB/s at best | the GPU and the CPU |

A kernel's inputs start in device memory and its outputs end there. Everything a kernel does in between, in registers and shared memory, is cheap by comparison.

## 3. Arithmetic intensity and the roofline

A kernel that performs $F$ FLOPs and moves $B$ bytes between device memory and the SMs cannot finish faster than either limit allows:
$$
t \;\ge\; \max\!\left(\frac{F}{P_{\text{peak}}},\; \frac{B}{\text{BW}}\right).
$$
Divide by $t$: the attainable throughput is $\min(P_{\text{peak}},\ \text{BW} \cdot I)$, where $I = F/B$ is the **arithmetic intensity** in FLOP per byte. On a log-log plot of throughput against intensity, this is a slanted line (the memory roof) meeting a flat line (the compute roof) at the **ridge point** $I^\star = P_{\text{peak}}/\text{BW}$. Kernels to the left are **memory-bound**; to the right, **compute-bound**.

::::derivation{id=d2 title="Ridge points of the T4"}
:::step
With tensor cores, $I^\star = 65 \times 10^{12} / 320 \times 10^9 \approx$ [[203.1|tol=0.5]] FLOP/byte.
:::
:::step
In fp32, $I^\star = 8.1 \times 10^{12} / 320 \times 10^9 \approx$ [[25.3|tol=0.2]] FLOP/byte. Half precision raises the compute roof eightfold but the memory roof only twofold (half the bytes per number).
:::
::::

## 4. Counting FLOPs and bytes

| Operation | FLOPs | Minimum bytes ($b$ per number) | Intensity |
| --- | --- | --- | --- |
| $C = AB$, $m \times k$ by $k \times n$ | $2mnk$ | $b(mk + kn + mn)$ | grows with size |
| elementwise op on $N$ values, $r$ inputs | a few per value | $b(r + 1)N$ | constant, below 1 |
| softmax over $N$ values | about $5N$ | $2bN$ | constant |

For square matrices, $I = 2n^3 / (3n^2 b) = 2n/(3b)$: large matrix products are compute-bound, and nothing else in a network is. A training step through linear layers costs the forward FLOPs plus twice that for the backward pass (gradients for inputs and for weights), which gives the rule of thumb of about **6 FLOPs per parameter per token**.

## 5. Tiling: how a matmul actually reaches high intensity

The minimum-bytes count assumes every input value is read from device memory once. A naive kernel, with each thread computing one output from a row of $A$ and a column of $B$, reads each value $n$ times. **Tiling** fixes this: a thread block computes a $T \times T$ block of $C$, streaming $T$-wide strips of $A$ and $B$ through shared memory, so each value it loads is reused $T$ times.

::::derivation{id=d3 title="Intensity of a tiled matmul"}
:::step
For $n \times n \times n$ with $T \times T$ output blocks, there are $(n/T)^2$ blocks, each reading $2nT$ values. Ignoring the output, the traffic is $2n^3/T$ values, so the intensity is $2n^3/(2n^3 b / T) = T/b$. In fp16 with $T = 64$ that is [[32]] FLOP/byte.
:::
:::step
To reach the fp16 ridge of about 203 FLOP/byte from device memory alone would need $T \approx 406$, and two $512 \times 512$ fp16 tiles occupy [[1048576]] bytes, sixteen times a T4 SM's 64 KB of shared memory.
:::
::::

Real matrix-multiplication libraries close the gap with reuse at other levels: blocks that run at the same time read overlapping strips, which the L2 cache serves, and each thread keeps a small tile of results in registers. The principle is the one derived here: reuse every value you load as many times as possible.

:::edge{to=L12 text="Tiling, shared memory and fusion become kernels you write in Triton."}
:::

## 6. Launch overhead, synchronization and transfers

The CPU issues kernels to the GPU through a queue. In eager PyTorch each operation costs on the order of ten microseconds of CPU time to dispatch and launch, so a kernel whose GPU work takes less than that is **launch-bound**: the GPU sits idle waiting for the next one. Normally the CPU runs ahead and the queue keeps the GPU busy, but any operation that needs a GPU result on the CPU, such as `.item()`, `print(loss)` or `if loss < x`, **synchronizes**: the CPU waits until the queue drains, and the overlap is lost.

Data also has to reach the GPU. A copy from ordinary host memory goes through a staging buffer; from **pinned** (page-locked) memory it can go directly and asynchronously with `non_blocking=True`, overlapping the next batch's copy with this batch's compute.

::::derivation{id=d4 title="Overheads"}
:::step
1000 kernels that each need 2 microseconds of GPU time, each launched with 10 microseconds of overhead, take about [[10]] ms rather than 2.
:::
:::step
A step needs 3 ms of CPU time to issue and 5 ms of GPU time. Overlapped, a step costs 5 ms; with a `.item()` at the end of every step it costs [[8]] ms.
:::
:::step
Copying 64 MiB ($64 \cdot 2^{20}$ bytes) at 12 GB/s takes about [[5.59|tol=0.05]] ms.
:::
::::

:::edge{to=L13 text="Attention's cost, read on this roofline: the score matrix is memory-bound."}
:::

:::edge{to=L17 text="Lower precision moves fewer bytes and unlocks the tensor cores."}
:::

:::edge{to=L18 text="Interconnect bandwidth plays the role of memory bandwidth when training spans GPUs."}
:::

:::edge{from=L08 text="the operations an autograd engine records and replays"}
:::

## 7. Measuring

Time GPU work only after synchronizing (`torch.cuda.synchronize()` or CUDA events), skip the first few warm-up calls, and report a median. `torch.profiler` records both the CPU operations and the GPU kernels, with their durations and counts: the tool for finding where a training step's time goes. The capstone notebook does all of this on a T4.
