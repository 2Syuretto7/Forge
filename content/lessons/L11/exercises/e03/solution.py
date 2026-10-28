import math


def tiled_matmul_bytes(n, tile, bytes_per=2):
    """Global-memory traffic of an n x n x n matmul computed in tile x tile output blocks: each
    block streams a tile-wide strip of A and of B (n * tile values each) and writes its result."""
    blocks = (n // tile) ** 2
    return bytes_per * (blocks * 2 * n * tile + n * n)


def tiled_intensity(n, tile, bytes_per=2):
    return 2 * n ** 3 / tiled_matmul_bytes(n, tile, bytes_per)


def min_tile_for_compute_bound(peak, bw, bytes_per=2):
    """Smallest power-of-two tile whose intensity (about tile / bytes_per) reaches the ridge point."""
    tile = 1
    while tile / bytes_per < peak / bw:
        tile *= 2
    return tile


def tile_smem_bytes(tile, bytes_per=2):
    """Shared memory to hold one tile of A and one of B (tile x tile each) at a time."""
    return 2 * tile * tile * bytes_per
