# Is it one-to-one?

A function can be inverted only where no two inputs share an output.

- `find_collision(f, xs, digits=9)`: return a pair `(a, b)` of different inputs from `xs` whose outputs agree after rounding to `digits` decimals, or `None` if all outputs are distinct. Use a dictionary from rounded output to the first input that produced it.
- `is_injective_on(f, xs)`: `True` when `find_collision` finds nothing.
- `largest_injective_interval(f, xs)`: scanning the sorted grid `xs`, the longest run of consecutive grid points on which `f` is strictly increasing or strictly decreasing; return its first and last points as a pair (the first such run if several are equally long).

## Hints

1. `key = round(f(x), digits)`; if the key is already in the dictionary, you have a collision.
2. A strictly monotone run never repeats an output, so it is injective.
3. Track the direction of each step `f(x[i+1]) - f(x[i])`; a run ends when the direction changes sign or is zero.
