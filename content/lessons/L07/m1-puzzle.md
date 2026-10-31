# Puzzle: the same FLOPs, a thousand times slower

A T4 GPU (the one Colab gives you) can perform 65 trillion half-precision floating-point operations per second on its tensor cores. Multiply two $4096 \times 4096$ matrices on it and you get close to that. Add two vectors of $2^{26}$ numbers and you get a tiny fraction of it.

::::predict{id=p1 kind=numeric answer=0.053 tol=0.01}
The T4 moves at most 320 GB/s between its memory and its cores. A half-precision vector addition reads 2 bytes from each input and writes 2 bytes per element, for one FLOP. What is the highest throughput it can reach, in TFLOP/s?

:::reveal
Each FLOP needs 6 bytes, so at 320 GB/s the addition can do at most $320 \times 10^9 / 6 \approx 5.3 \times 10^{10}$ FLOP/s, about 0.053 TFLOP/s: less than a tenth of a percent of the peak. Its speed is set entirely by memory bandwidth. Most operations in a neural network, everything except matrix products and convolutions, are like this.
:::
::::

::::predict{id=p2 kind=numeric answer=8.14 tol=0.2}
The T4 has 40 streaming multiprocessors, each with 64 fp32 cores, running at up to 1.59 GHz, and each core completes one fused multiply-add (2 FLOPs) per cycle. What is its peak fp32 throughput in TFLOP/s?

:::reveal
$40 \times 64 \times 1.59 \times 10^9 \times 2 \approx 8.14 \times 10^{12}$ FLOP/s, the 8.1 TFLOP/s on the datasheet. The 65 TFLOP/s figure comes from the separate tensor cores, which multiply small half-precision matrices in one instruction.
:::
::::

Explore the two limits in the widget: change the matrix size and the precision, and watch which kernels sit under the slanted memory roof and which reach the flat compute roof.

:::widget{name=Roofline hardware=t4 precision=fp16}
:::
