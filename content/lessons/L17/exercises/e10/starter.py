def amdahl_speedup(fractions, speedups):
    """Overall speedup when each part of the run (fractions of the original time, summing to 1) is
    sped up by its own factor."""
    raise NotImplementedError


def t4_part_speedups():
    """On a T4, matrix products move from 8.1 fp32 TFLOP/s to 65 fp16 tensor-core TFLOP/s; memory-bound
    operations move half the bytes. Return (matmul speedup bound, memory-bound speedup)."""
    raise NotImplementedError
