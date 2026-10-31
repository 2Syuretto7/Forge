# Placing kernels on the roofline

The kernels of a transformer layer span three orders of magnitude of arithmetic intensity (Section 1, and L07). With the conventions below, in fp32 (4 bytes per number), compute each kernel's flops and minimal bytes, and place it on a chip's roofline.

| Kernel | Flops | Numbers moved |
| --- | --- | --- |
| `add(n)` | $n$ | $3n$ |
| `matvec(m, n)` | $2mn$ | $mn + n + m$ |
| `matmul(m, n, k)` | $2mnk$ | $mk + kn + mn$ |
| `softmax(r, c)` | $5rc$ (max, subtract, exp, sum, divide) | $2rc$ |
| `layernorm(r, c)` | $8rc$ | $2rc + 2c$ |

- `profile(name, *dims)`: `(flops, bytes)` for the kernel named by the first column.
- `place(name, dims, peak, bw)`: a dict with `"intensity"`, `"attainable"`, `"bound"` and `"time"`, as in e02.

The tests place each kernel on the T4 in fp32 and confirm that only the large matmul reaches the compute roof, and that a batch-1 forward pass through a $4096 \times 4096$ layer (a matrix-vector product) runs more than 50 times slower per flop than a batch of 4,096 tokens (a matmul).

## Hints

1. Intensity is a property of the kernel and its sizes, not of the chip; the bound depends on both.
2. Elementwise kernels have an intensity below 1 at any size.
3. Batching turns many matrix-vector products into one matrix product, and that is why inference servers batch requests.
