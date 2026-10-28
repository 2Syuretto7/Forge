# Paged KV memory

Reserving the maximum context for every sequence wastes most of the cache, because most sequences end early. PagedAttention (vLLM, 2023) stores each sequence's cache in fixed-size pages allocated as it grows, like virtual memory.

1. `pages_needed(tokens, block)`.
2. `paged_waste(lengths, block)`: unused token slots when every sequence holds whole pages.
3. `contiguous_waste(lengths, max_len)`: unused slots when every sequence reserves `max_len`.

## Hints

1. A sequence wastes at most `block - 1` slots in its last page.
2. Pages need not be contiguous: a table maps each sequence's logical pages to physical ones.
3. Less waste means more sequences in the same memory, which means a larger batch and higher throughput.
