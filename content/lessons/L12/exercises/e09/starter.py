def flash_smem_bytes(block_m, block_n, d, bytes_per=2):
    """On-chip bytes of one FlashAttention program: a Q tile (block_m x d), a K and a V tile
    (block_n x d each) in the input precision, and an fp32 accumulator (block_m x d) and score tile
    (block_m x block_n)."""
    raise NotImplementedError


def best_blocks(d, budget, sizes=(16, 32, 64, 128), bytes_per=2):
    """Among square blocks block_m = block_n from `sizes`, the largest that fits the budget."""
    raise NotImplementedError
