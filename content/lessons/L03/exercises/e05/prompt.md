# The spiral dataset

Generate the three-arm spiral of the puzzle and a helper to measure accuracy.

- `make_spiral(n_per_class, K, seed)`: for class $j$, radii `np.linspace(0, 1, n)` and angles `np.linspace(4j, 4(j+1), n) + 0.2 * noise`, points $(r\sin t, r\cos t)$. Draw the noise per class, in class order, from one `np.random.default_rng(seed)`. Return `X` `(n K, 2)` and integer labels `y`, class by class.
- `accuracy(pred, y)`.
- `linear_baseline(X, y, steps, lr)`: softmax regression trained by full-batch gradient descent from zero; return its training accuracy.

The test confirms the puzzle: the linear model stays far below 100 percent.

## Hints

1. `np.column_stack([r * np.sin(t), r * np.cos(t)])`.
2. Reuse your softmax regression from L01.
3. 2,000 steps with `lr=1` is plenty for the linear model.
