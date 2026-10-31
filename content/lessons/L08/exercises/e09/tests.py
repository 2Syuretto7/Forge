import sub


def test_bytes():
    assert sub.flash_smem_bytes(64, 64, 64) == 57344
    assert sub.flash_smem_bytes(16, 32, 8, bytes_per=4) == (16 * 8 + 2 * 32 * 8) * 4 + 4 * (16 * 8 + 16 * 32)


def test_best_blocks():
    assert sub.best_blocks(64, 64 * 1024) == 64
    assert sub.best_blocks(128, 64 * 1024) == 32
    assert sub.best_blocks(64, 228 * 1024) == 128
    assert sub.best_blocks(512, 1024) is None
