# Per-SM limits of NVIDIA Turing GPUs (compute capability 7.5), the T4's architecture.
TURING = {"max_threads": 1024, "max_warps": 32, "max_blocks": 16, "registers": 65536, "smem": 65536, "warp": 32}


def peak_flops(sms, cores_per_sm, clock_hz, flops_per_core_cycle=2):
    """Each core retires one fused multiply-add (2 FLOPs) per cycle."""
    raise NotImplementedError


def blocks_per_sm(threads_per_block, regs_per_thread, smem_per_block, lim=TURING):
    """Resident blocks per SM: the tightest of the thread, warp, block, register and shared-memory limits."""
    raise NotImplementedError


def occupancy(threads_per_block, regs_per_thread, smem_per_block, lim=TURING):
    """Active warps per SM as a fraction of the maximum."""
    raise NotImplementedError
