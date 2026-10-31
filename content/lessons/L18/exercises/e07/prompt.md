# int8 weights

Decoding is memory-bound, so halving the bytes per weight nearly halves the step time. Weight-only quantization stores each weight in 8 bits with a scale per output row.

1. `quantize_int8(W)`: each row's scale is its largest absolute value divided by 127; weights round to integers in $[-127, 127]$. Return the int8 array and the scales.
2. `dequantize(q, scale)`.
3. `int8_matmul(x, q, scale)`: $x W^\top$ computed with the integers, scaling each output column afterwards.

## Hints

1. Guard rows of zeros: give them scale 1.
2. The rounding error of each weight is at most half its row's scale.
3. Scaling after the product is exact because each output column uses one row's scale.
