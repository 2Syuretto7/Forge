# Data-parallel SGD

Every rank holds a shard $(X_r, y_r)$ of the batch and the same weights. Each computes its local gradient; the gradients are combined; every rank applies the same update, so the weights stay identical without ever being sent.

1. `local_loss_grad(w, X, y)`: the loss $\tfrac12 \operatorname{mean}((Xw - y)^2)$ on one shard and its gradient.
2. `dp_step(w, shards, lr)`: one synchronous step whose gradient equals the full-batch gradient, even when shards differ in size.

## Hints

1. The gradient is $X^\top (Xw - y)/n$ for a shard of $n$ examples.
2. The full-batch gradient is the size-weighted average of the shard gradients: $\sum_r n_r g_r / \sum_r n_r$.
3. In practice the shards are equal and the all-reduce averages; exercise 12 shows what goes wrong when they are not.
