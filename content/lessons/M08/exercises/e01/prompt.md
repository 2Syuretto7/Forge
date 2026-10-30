# The product and sum rules

- `count_strings(alphabet, length)`: strings of the given length over an alphabet of `alphabet` symbols, repetition allowed.
- `count_distinct_strings(alphabet, length)`: the same with no symbol used twice (0 if impossible).
- `count_either(*sizes)`: the number of options when a choice is made from one of several disjoint groups with the given sizes.
- `count_staged(*sizes)`: the number of outcomes of a choice in stages with the given numbers of options per stage.

## Hints

1. `alphabet ** length`.
2. Multiply `alphabet`, `alphabet - 1`, ... for `length` factors.
3. The sum rule adds; the product rule multiplies.
