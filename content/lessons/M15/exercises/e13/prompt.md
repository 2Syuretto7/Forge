# A difference quotient at a corner

- `estimates_at_zero(f, h)`: the forward, backward and central differences of `f` at 0 with step `h`, as a dictionary with keys `"forward"`, `"backward"`, `"central"`.
- `looks_differentiable(f, a, hs=(1e-2, 1e-4, 1e-6))`: whether the forward and backward differences agree to within $10^{-3}$ at every step in `hs`.

For $|x|$ the central difference at 0 is exactly 0, a perfectly plausible derivative, while the forward and backward ones are $1$ and $-1$ at every step. Only comparing the sides reveals the corner.

## Hints

1. Backward: $(f(0) - f(-h))/h$.
2. The central difference is the average of the forward and backward ones.
3. For the ReLU at 0 the central difference is $1/2$.
