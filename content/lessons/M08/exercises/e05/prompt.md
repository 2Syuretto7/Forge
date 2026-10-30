# Exact probabilities by counting

A sample space is a list of equally likely outcomes, and an event is a predicate on outcomes.

- `probability(event, space)`: the exact probability as a `Fraction`.
- `dice_space(n)`: all ordered outcomes of rolling `n` six-sided dice, as tuples (use `itertools.product`).
- `complement(event)`: the event "not `event`", as a new predicate.
- `p_at_least_one_six(n)`: exactly, by the complement: $1 - (5/6)^n$ as a `Fraction`.

## Hints

1. `Fraction(sum(1 for w in space if event(w)), len(space))`.
2. `list(itertools.product(range(1, 7), repeat=n))`.
3. `lambda w: not event(w)`.
