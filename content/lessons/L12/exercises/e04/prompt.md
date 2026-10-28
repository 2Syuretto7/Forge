# What fusion saves

1. `softmax_traffic(rows, cols, bytes_per=2, fused=True)`: bytes moved by a row softmax, counting 6 array passes when unfused (as in the derivation) and 2 when fused.
2. `predicted_speedup(rows, cols, bytes_per=2)`: the ratio, which is what a memory-bound kernel gains.
3. `fits_on_chip(cols, bytes_per=4, budget=64 * 1024)`: whether one row, held in fp32, fits a program's on-chip budget. Rows longer than that need the online softmax instead of a single block.

## Hints

1. Each array pass is `rows * cols * bytes_per` bytes.
2. The ratio does not depend on the shape.
3. 64 KB holds 16,384 fp32 values.
