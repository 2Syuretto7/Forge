# The memory price of reverse mode

Reverse mode stores the activations of the forward pass. For a network of `depth` layers of `width` units and a batch of `batch` examples, in float32:

- `activation_bytes(depth, width, batch)`: $4 \cdot \text{depth} \cdot \text{width} \cdot \text{batch}$.
- `checkpoint_bytes(depth, width, batch, k)`: with **checkpointing**, only every $k$-th activation is stored, and each segment of $k$ layers is recomputed during the backward pass and held while it is processed: $4 \cdot (\lceil \text{depth}/k \rceil + k) \cdot \text{width} \cdot \text{batch}$.
- `best_k(depth)`: the $k$ that minimizes $\lceil \text{depth}/k \rceil + k$ (the smallest such $k$), about $\sqrt{\text{depth}}$.
- `extra_compute(k)`: the fraction of forward work added by recomputation, about one extra forward pass: return 1.0 for $k > 1$ and 0.0 for $k = 1$.

## Hints

1. Integers throughout for bytes.
2. Search $k$ from 1 to `depth`.
3. Checkpointing trades one extra forward pass for memory that grows like $\sqrt{\text{depth}}$ instead of depth.
