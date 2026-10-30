# A batch of products, timed

- `batched_loop(A, B)`: for stacks of shapes `(b, m, n)` and `(b, n, p)`, multiply pair by pair in a Python loop, `A[i] @ B[i]`, and stack the results.
- `batched(A, B)`: the same with one call, `A @ B`.
- `measure(b, n, seed=0)`: build two random float32 stacks of shape `(b, n, n)`, time `batched` once with `time.perf_counter`, and return `(flops, seconds, flops / seconds)` where `flops` is $2bn^3$.

Try `measure(64, 256)` in the console, then `measure(64, 512)` if you can wait a few seconds: $1.7 \times 10^{10}$ operations. Your browser runs NumPy without the multithreaded libraries of a server, so expect a few billion operations per second at best; a laptop's native NumPy does tens of billions, a GPU tens of trillions.

## Hints

1. `np.stack([A[i] @ B[i] for i in range(len(A))])`.
2. `rng.standard_normal((b, n, n), dtype=np.float32)`.
3. Time only the multiplication, not the creation of the arrays.
