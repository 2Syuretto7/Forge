# The core tensor

Now the engine for arrays. A `Tensor` holds `data` (a float NumPy array), `grad` (`None` until a gradient arrives), `_parents` and a `_backward` closure. `_accumulate(g)` (given) adds a gradient contribution.

Implement:

- `__add__` and `__mul__`, elementwise with NumPy broadcasting; their backward rules must **unbroadcast** (the function from the previous exercise is provided).
- `sum(axis=None, keepdims=False)`: its backward broadcasts the gradient back to the input's shape (when `keepdims=False` and an axis was given, first restore the summed axis with `np.expand_dims`).
- `backward()`: build a topological order of the graph that ends at this tensor, reset the gradients of non-leaf tensors (those with parents) to `None`, set this tensor's gradient to ones, and call each `_backward` in reverse order, skipping tensors that received no gradient.

Use an iterative depth-first search in `backward`: graphs from real training loops are deeper than Python's recursion limit.

## Hints

1. In `__add__`: `out = Tensor(self.data + other.data, (self, other), "add")`, then a closure that calls `self._accumulate(unbroadcast(out.grad, self.shape))` and the same for `other`.
2. Wrap plain numbers and arrays with `as_tensor` so `t * 2.0` works.
3. An iterative post-order: push `(node, False)`; when popped, push `(node, True)` and then its unvisited parents; append a node to the order when it is popped with `True`.
