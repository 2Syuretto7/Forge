# Per-SM limits of NVIDIA Turing GPUs (compute capability 7.5), the T4's architecture.
TURING = {"max_threads": 1024, "max_warps": 32, "max_blocks": 16, "registers": 65536, "smem": 65536, "warp": 32}


def peak_flops(sms, cores_per_sm, clock_hz, flops_per_core_cycle=2):
    """Each core retires one fused multiply-add (2 FLOPs) per cycle."""
    return sms * cores_per_sm * clock_hz * flops_per_core_cycle


def blocks_per_sm(threads_per_block, regs_per_thread, smem_per_block, lim=TURING):
    """Resident blocks per SM: the tightest of the thread, warp, block, register and shared-memory limits."""
    warps = -(-threads_per_block // lim["warp"])
    limits = [lim["max_blocks"], lim["max_warps"] // warps, lim["registers"] // (regs_per_thread * warps * lim["warp"])]
    if smem_per_block:
        limits.append(lim["smem"] // smem_per_block)
    return min(limits)


def occupancy(threads_per_block, regs_per_thread, smem_per_block, lim=TURING):
    """Active warps per SM as a fraction of the maximum."""
    warps = -(-threads_per_block // lim["warp"])
    return blocks_per_sm(threads_per_block, regs_per_thread, smem_per_block, lim) * warps / lim["max_warps"]
