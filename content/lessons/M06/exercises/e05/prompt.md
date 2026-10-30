# Growth and decay

Use `math.log` and `math.exp` freely now.

- `doubling_time(rate)`: years for something growing by the fraction `rate` per year (compounded yearly) to double: solve $(1 + r)^t = 2$.
- `continuous_doubling_time(r)`: the same for continuous growth $e^{rt}$.
- `rule_of_70(percent)`: the approximation $70 / \text{percent}$.
- `half_life(k)`: the time for $e^{-kt}$ to fall to one half.
- `growth_factor(r, years)`: $e^{r \cdot \text{years}}$.

## Hints

1. Take logarithms: $t \ln(1 + r) = \ln 2$.
2. $e^{rt} = 2$ gives $t = \ln 2 / r$.
3. The rule of 70 works because $100 \ln 2 \approx 69.3$.
