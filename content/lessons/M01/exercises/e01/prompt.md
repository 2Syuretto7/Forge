# Python as a calculator

Python is a calculator that remembers. You write **functions**: a function has a name, takes inputs (its arguments) and **returns** an output. In the editor, each function looks like this:

```python
def seconds_in_days(days):
    """A docstring says what the function does."""
    return days * 24 * 60 * 60
```

The arithmetic operators are `+`, `-`, `*` (times), `/` (divide), and `**` (power: `2 ** 10` is 1024). Parentheses group as in ordinary arithmetic. A list of numbers is written `[3, 1, 4]`; `sum(xs)` adds a list and `len(xs)` counts its items.

Write four functions:

- `seconds_in_days(days)`: the number of seconds in that many days.
- `average(xs)`: the mean of a non-empty list of numbers.
- `percent_change(old, new)`: the change from `old` to `new` as a percentage of `old` (from 50 to 60 is 20.0).
- `compound(amount, rate, years)`: `amount` growing by the fraction `rate` each year for `years` years (100 at 0.1 for 2 years is 121.0).

Press **Run code** to try things (use `print(...)` to see values), and **Submit answer** to run the hidden tests.

## Hints

1. A day is 24 hours of 60 minutes of 60 seconds.
2. The mean is the sum divided by the count: `sum(xs) / len(xs)`.
3. Growing by a fraction `rate` multiplies by `1 + rate`; doing it `years` times multiplies by `(1 + rate) ** years`.
