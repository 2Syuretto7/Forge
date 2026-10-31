# The chain rule as forward accumulation

A program that applies functions one after another, $x \to g_1(x) \to g_2(g_1(x)) \to \cdots$, has derivative $\prod_k g_k'(\cdot)$ evaluated along the way. Implement both accumulation orders for a chain of scalar functions, given as a list of `(g, dg)` pairs.

- `forward_accumulate(chain, x)`: walk forward, carrying `(value, derivative)`; return both at the end.
- `reverse_accumulate(chain, x)`: first run forward, storing every intermediate input; then walk backward multiplying local derivatives. Return `(value, derivative)` and make sure you call each `dg` exactly once.
- `stored_values(chain, x)`: the list of intermediate inputs the reverse pass must remember (one per function).

Both orders give the same number; reverse needs memory for the stored values. That memory is what L04 and L14 have to manage.

## Hints

1. Forward: `d = dg(v) * d; v = g(v)`, in that order.
2. Reverse: save `v` before applying each `g`, then loop over the saved list backwards.
3. The stored list has one entry per function.
