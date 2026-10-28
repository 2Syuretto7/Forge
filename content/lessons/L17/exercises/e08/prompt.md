# Master weights

1. `mse_grad(w, X, y)`: $L = \tfrac12 \operatorname{mean}((Xw - y)^2)$ and its gradient.
2. `train(X, y, lr, steps, master)`: gradient descent where the forward and backward passes use float16 copies of the weights and data. With `master=True`, keep a float32 master copy that receives every update and is cast to float16 for the next step; with `master=False`, keep only the float16 weights and round every update into them. Return the final loss, computed in float64.

## Hints

1. Start from zero weights.
2. `lr * g` is often smaller than half the fp16 spacing of the weight it updates; that is what the master copy rescues.
3. Compute the gradient in float32 from the float16 copies.
