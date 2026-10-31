# How a residual stream grows

1. `residual_rms(depth, alpha, branch="linear", width=256, batch=256, seed=0)`: start from unit-normal `h` of shape `(batch, width)` drawn from `np.random.default_rng(seed)`, apply `depth` layers $h \leftarrow h + \alpha F(h)$ with fresh weights from the same generator, and return the root mean square of `h` before the first layer and after each one. The branch is $F(h) = hW$ with $W \sim \mathcal N(0, 1/\text{width})$ for `"linear"`, or $\operatorname{relu}(hW)$ with He-initialized $W$ for `"relu"`.
2. `predicted_growth(depth, alpha)`: $(1 + \alpha^2)^{\text{depth}/2}$.

Compare the two branches with the prediction. The linear branch follows it; the ReLU branch, whose outputs are all positive, grows much faster.

## Hints

1. Draw `h` first, then one weight matrix per layer, in order.
2. `branch == "linear"`: `h = h + alpha * (h @ W)`.
3. The ratio `rms[-1] / rms[0]` is what the prediction describes.
