import numpy as np
import sub


def test_paging():
    assert sub.pages_needed(1, 16) == 1 and sub.pages_needed(16, 16) == 1 and sub.pages_needed(17, 16) == 2
    lengths = [5, 100, 37, 2048, 300]
    assert sub.paged_waste(lengths, 16) == sum(-n % 16 for n in lengths)
    assert sub.paged_waste(lengths, 16) < 16 * len(lengths)
    assert sub.contiguous_waste(lengths, 2048) > 50 * sub.paged_waste(lengths, 16)
