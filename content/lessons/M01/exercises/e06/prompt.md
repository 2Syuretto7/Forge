# Converting units with a table

The starter defines a table `UNITS` mapping each unit to its dimension and its size in a base unit: seconds for time, bytes for data, FLOPs for work. For example `UNITS["h"] == ("time", 3600)` and `UNITS["GiB"] == ("data", 2 ** 30)`.

- `convert(value, frm, to)` converts `value` from unit `frm` to unit `to`. Converting between different dimensions (hours to bytes) raises `ValueError`.
- `percent_bigger(a, b)` returns how much bigger unit `a` is than unit `b` of the same dimension, in percent: `percent_bigger("GiB", "GB")` is about 7.37.
- `best_unit(value, unit)` re-expresses a quantity in the unit of the same dimension that gives the smallest result of at least 1 (so 7,200 s becomes `(2.0, "h")`, and 0.5 s stays in seconds as `(0.5, "s")`). Return the pair `(number, unit)`.

The tests check an **invariant**: converting from `a` to `b` and back returns the original value, for every pair of units of the same dimension.

## Hints

1. Convert to the base unit by multiplying by the size of `frm`, then divide by the size of `to`.
2. `100 * (size_a / size_b - 1)`.
3. Loop over the units of the right dimension, convert to each, and keep the smallest result that is at least 1; if there is none, keep the smallest unit.
