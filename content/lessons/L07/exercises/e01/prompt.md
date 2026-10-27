# The linear layer, forward and backward

Implement a fully connected layer $Y = XW + b$ for a batch `X` of shape `(B, n_in)`, weights `W` `(n_in, n_out)` and bias `b` `(n_out,)`.

- `linear_forward(X, W, b)` returns `(Y, cache)`, where `cache` holds whatever the backward pass needs.
- `linear_backward(dY, cache)` returns `(dX, dW, db)`.

The tests check every gradient against central differences of the scalar $L = \sum Y \odot G$ for a random $G$, whose gradient with respect to $Y$ is exactly $G$.

## Hints

1. Cache `(X, W)`.
2. `dX = dY @ W.T`, `dW = X.T @ dY`, `db = dY.sum(axis=0)`.
3. Check shapes first: each gradient has the shape of the thing it differentiates.
