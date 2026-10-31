import sub


def test_traffic():
    assert sub.tiled_matmul_bytes(1024, 64) == 2 * ((1024 // 64) ** 2 * 2 * 1024 * 64 + 1024 ** 2)
    assert sub.tiled_matmul_bytes(8, 8, bytes_per=4) == 4 * (2 * 8 * 8 + 64)


def test_intensity_close_to_tile_over_bytes():
    i = sub.tiled_intensity(4096, 64)
    assert 31 < i < 32


def test_min_tile_and_shared_memory():
    t = sub.min_tile_for_compute_bound(65e12, 320e9)
    assert t == 512
    assert sub.tile_smem_bytes(t) == 1 << 20
    assert sub.min_tile_for_compute_bound(8.1e12, 320e9, bytes_per=4) == 128
    assert sub.tile_smem_bytes(64) <= 64 * 1024
