# Summing 100 million numbers

Stream $10^8$ uniform float32 numbers from `np.random.default_rng(seed).random(chunk, dtype=np.float32)`, 100 chunks of a million, and keep six running totals:

- `"float16"`, `"float32"` and `"float64"`: sequential sums in each type, carried from chunk to chunk.
- `"pairwise32"`: each chunk summed by NumPy's `np.sum` in float32 (which is pairwise inside), the chunk totals added pairwise in float32 at the end.
- `"kahan32"`: e08's vectorized Kahan sum, with its running sums and compensations carried across chunks.
- `"exact"`: `math.fsum` of the chunk sums computed in float64, accurate to the last digit.

Implement `stream_sums(n_chunks=100, chunk=10**6, seed=0)` returning that dictionary, and `errors(sums)`: the absolute error of each method against `"exact"`.

The tests expect the float16 sum stuck at 2,048, the float32 sum stuck near $2^{24} \approx 1.68 \times 10^7$ while the truth is $5 \times 10^7$, and the compensated sums within a few units.

## Hints

1. Carry a sequential sum across chunks with `np.cumsum(np.concatenate([[carry], x]), dtype=...)[-1]`.
2. For Kahan, reshape each chunk to `(chunk // width, width)` and keep `s` and `c` between chunks.
3. Float16 overflows nothing here: it stalls at 2,048 long before its maximum, 65,504.
