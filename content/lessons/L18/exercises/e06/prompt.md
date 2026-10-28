# A tensor-parallel MLP

Megatron-LM splits a transformer's MLP over $t$ GPUs without communicating inside it. The first layer is split by **columns**: rank $r$ computes its own slice of the hidden units, $h_r = \operatorname{ReLU}(x W_{1,r} + b_{1,r})$, and since ReLU is elementwise no exchange is needed. The second layer is split by **rows**: rank $r$ multiplies its hidden slice by its rows $W_{2,r}$, giving a partial output; one all-reduce sums the partial outputs.

1. `tp_mlp_forward(x, W1s, b1s, W2s, b2)`: return $y = \sum_r h_r W_{2,r} + b_2$ and a cache.
2. `tp_mlp_backward(dy, cache, W1s, W2s)`: per-rank $(\partial W_{1,r}, \partial b_{1,r}, \partial W_{2,r})$, the shared $\partial b_2$, and $\partial x$, which is again a sum over ranks.

## Hints

1. The cache needs $x$, each rank's pre-activation $z_r$ and hidden slice $h_r$.
2. $\partial W_{2,r} = h_r^\top dy$ and $\partial z_r = (dy\, W_{2,r}^\top) \odot [z_r > 0]$.
3. Forward needs one all-reduce (of $y$), backward one (of $\partial x$): two per MLP per pass, whatever $t$.
