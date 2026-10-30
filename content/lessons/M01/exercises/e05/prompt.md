# A quantity that knows its units

Dimensional analysis by computer: a `Quantity` stores a number and its units, multiplies and divides them like algebra, and refuses to add things of different kinds.

Units are a dictionary from unit name to power: metres per second is `{"m": 1, "s": -1}`, a plain number is `{}`. Write the class:

- `Quantity(value, units)` stores `self.value` and `self.units`, dropping any unit whose power is 0. `units` may be omitted, meaning no units.
- `a * b` and `a / b` multiply or divide the values and add or subtract the powers. A plain number on either side just scales: `2 * q`, `q * 2`, `q / 2`.
- `a + b` and `a - b` work only when the units are equal; otherwise raise `ValueError("cannot add ...")`.
- `a == b` is true when the units are equal and the values agree to a relative tolerance of `1e-12` (use `math.isclose`).

A class groups data with the functions that act on it. The special method names (`__mul__`, `__add__` and friends) are how Python lets `a * b` call your code. The starter lists every one you need, with its job in the docstring. `isinstance(x, Quantity)` tells you whether `x` is a quantity or a plain number.

The tests include an **invariant**: for random quantities `a` and `b`, `(a * b) / b == a`, units and all.

## Hints

1. Copy the units into a new dictionary when you combine them: `out = dict(self.units)`, then add or subtract powers with `out[k] = out.get(k, 0) + p`.
2. Remove zero powers with `{k: p for k, p in out.items() if p != 0}`.
3. `__rmul__` handles `2 * q`; it can simply return `self * other`.
