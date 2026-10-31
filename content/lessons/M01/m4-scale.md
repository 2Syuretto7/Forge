# Scale: GPU-hours, browser throughput and memory

The build movement gave you tools. Now use them at realistic sizes: estimate a training run, measure your own machine, and size a model's memory.

## A pretraining run on paper

The ladder below is set up for a 100-million-parameter model trained on 2 billion tokens. Adjust each factor's range to your own belief before you look at the computed value.

:::widget{name=MagnitudeLadder preset=train}
:::

:::exercise{ref=e10}
:::

## Measure your own machine

Your browser runs Python through WebAssembly, which is slower than native code but fast enough to measure. The exercise times matrix multiplications and converts the time into FLOPs per second.

::::predict{id=p4 kind=choice answer=b}
Python in the browser multiplies two $128 \times 128$ matrices with NumPy. Which range do you expect for its throughput?

- Below $10^6$ FLOP/s, a million.
- Between $10^7$ and $10^{10}$ FLOP/s.
- Between $10^{12}$ and $10^{14}$ FLOP/s, like a GPU.

:::reveal
Typically between $10^8$ and $10^{10}$: a few hundred million to a few billion FLOPs per second on one CPU core, without the vector units and many cores that native libraries exploit. A data-centre GPU is about $10^5$ times faster, which is the gap that GPU lessons (L07) are about. Whatever your number, the estimate-then-measure habit is the point: the factor between them tells you how good your model of the machine is.
:::
::::

:::exercise{ref=e11}
:::

## Memory

Parameters must also fit in memory. A model's weights at 2 bytes each are the easy part; training with the Adam optimizer in mixed precision keeps about 16 bytes per parameter (two each for the weights and gradients in 16-bit, four each for a 32-bit master copy of the weights and two optimizer statistics).

:::exercise{ref=e12}
:::
