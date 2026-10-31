# L2 penalty and gradient clipping

The L03 network is provided: `init`, `loss_and_grads` and `evaluate`.

1. `loss_and_grads_l2(params, X, y, lam)`: the L03 loss plus $\tfrac{\lambda}{2}\sum \lVert W \rVert^2$ over the weight matrices only, with its gradients.
2. `global_norm(grads)`: the Euclidean norm of all gradient entries together.
3. `clip_by_global_norm(grads, max_norm)`: if the global norm exceeds `max_norm`, scale every gradient by the same factor so that it equals `max_norm`; otherwise return the gradients unchanged. Clipping by the global norm keeps the update's direction, which clipping each entry separately would not.

## Hints

1. Call `loss_and_grads` first, then add the penalty and `lam * W` for keys starting with `"W"`.
2. Return a new dictionary from `clip_by_global_norm`; do not modify the input.
3. Large-model training clips at a global norm of about 1; L15 shows why.
