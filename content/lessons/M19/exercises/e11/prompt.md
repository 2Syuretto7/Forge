# Twenty layers, both modes

The starter's `make_net(n, width=32, depth=20, seed=0)` returns weight matrices for $f(x) = w^\top h_{20}$ with $h_k = \tanh(W_k h_{k-1})$, $h_0 = x \in \mathbb{R}^n$, a scalar output.

- `forward_mode_grad(Ws, w, x)`: push the $n \times n$ identity through the layers as a tangent matrix (all $n$ JVPs at once): $T_k = \operatorname{diag}(1 - h_k^2) W_k T_{k-1}$, and the gradient is $w^\top T_{20}$.
- `reverse_mode_grad(Ws, w, x)`: one forward pass storing the $h_k$, then one backward pass of VJPs from $\bar h_{20} = w$.
- `time_ratio(n)`: the time of the forward-mode gradient over the reverse-mode one, for a random input of length `n`.

Forward mode's work grows with $n$ (its tangent matrix has $n$ columns); reverse mode's does not.

## Hints

1. $T_0 = I_n$; each layer multiplies a $32 \times 32$ matrix by a $32 \times n$ one, except the first, $32 \times n$ by $n \times n$.
2. Backward: $\bar a_k = \bar h_k \odot (1 - h_k^2)$, then $\bar h_{k-1} = W_k^\top \bar a_k$.
3. Time each with several repetitions.
