# Coalescing

Thread $t$ of a warp loads the element at byte address $t \cdot \text{stride} \cdot \text{elem\_bytes}$.

1. `transactions(stride, n_threads=32, elem_bytes=4, segment=32)`: the number of distinct aligned `segment`-byte blocks the warp touches.
2. `efficiency(...)`: the bytes the threads use divided by the bytes transferred.

## Hints

1. A segment is identified by `address // segment`; count the distinct ones with a set.
2. Stride 1 with fp32 is perfectly coalesced: efficiency 1.
3. Once the stride is at least `segment / elem_bytes`, every thread needs its own segment.
