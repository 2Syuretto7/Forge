# What finite differences cost

A function of $n$ inputs has $n$ partial derivatives, one per input (M18).

- `evaluations(n, method)`: function evaluations for all of them: $n + 1$ for `"forward"` (one shared base point), $2n$ for `"central"`.
- `seconds(n, method, eval_seconds)`: the time at a given cost per evaluation.
- `days_for_model(params, eval_seconds)`: central differences for a model with `params` parameters, in days.

A model with $10^8$ parameters whose loss takes 0.1 s to evaluate needs $2 \times 10^7$ seconds, about 231 days, for one gradient by central differences. Reverse-mode automatic differentiation (M19) gets it for the cost of about two evaluations.

## Hints

1. Plain arithmetic.
2. A day has 86,400 seconds.
3. Return floats from the time functions.
