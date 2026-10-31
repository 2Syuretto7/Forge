# Capstone: profile and fix a slow training step

Open the Colab notebook with a **T4 GPU** runtime and run it top to bottom. You will:

1. Fill in the FLOP and byte counts of the benchmarked matrix products and additions, and see them on the T4's roofline.
2. Measure pageable and pinned host-to-device copies.
3. Profile the provided `slow_step` with `torch.profiler` and count its kernels per step.
4. Write `prepare`, `make_optimizer` and `fast_step` so that the training step runs at least twice as fast and produces the same losses (within half-precision rounding).
5. Write a report of at least 80 words: what the profile showed, what you changed, and the measured speedup.

The autograder cell prints a completion code; the speedup test runs only on a GPU, so a CPU run cannot produce the full code.
