# Clipping by the global norm

1. `global_norm(grads)`: the L2 norm of all gradient arrays together, as if flattened into one vector.
2. `clip_by_global_norm(grads, max_norm)`: scale every gradient by $\min(1, \text{max\_norm}/\|g\|)$, and return the clipped list and the norm before clipping.

## Hints

1. $\|g\| = \sqrt{\sum_i \sum g_i^2}$ over all arrays.
2. One factor for all arrays keeps the update's direction; clipping each array separately would change it.
3. Log the norm before clipping every step: its spikes come before the loss spikes.
