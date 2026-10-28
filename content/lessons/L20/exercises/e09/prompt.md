# Packing examples

Instruction data is short and uneven. Rather than padding every example to the longest, pack several into one sequence, and keep them from seeing each other.

1. `packed_attention_mask(lengths)`: position $i$ may attend to $j$ only if $j \le i$ and both belong to the same example; return a boolean $T \times T$ array.
2. `packed_positions(lengths)`: position ids restarting at 0 for each example.

## Hints

1. Give every position its example's index with `np.repeat`, then compare the indices pairwise.
2. Combine with the causal mask `np.tril`.
3. Without the mask, the second example in a pack would condition on the first, which never happens at inference.
