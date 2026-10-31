# The online softmax

1. `online_softmax(x, block=4)`: one pass over `x` in blocks, keeping the running maximum `m` (starting at $-\infty$) and the running sum `l` of $e^{x_j - m}$ (starting at 0), rescaling `l` by $e^{m_{\text{old}} - m_{\text{new}}}$ whenever the maximum grows. Return `(p, m, l)` with `p = exp(x - m) / l`.
2. `merge(m1, l1, m2, l2)`: combine the summaries of two disjoint parts of a vector into the summary of the whole.

## Hints

1. `np.exp(-np.inf - finite)` is 0, so the first block needs no special case.
2. Update `m` only after rescaling `l`.
3. The merged summary must not depend on the order of the two parts.
