# Explain it plainly: the speedometer

Explain what a derivative is using a car's speedometer and nothing else.

Guidelines:

- Write 150 to 400 words.
- No formulas.
- Say how the reading is related to distance and time.
- Say what happens at a sudden stop.

:::feynman{id=f1 prompt="Explain what a derivative is using a car's speedometer and nothing else." key_points="The speedometer shows how fast the distance travelled is changing at this instant|An average speed is distance over time for a whole stretch of the trip|Over shorter and shorter stretches the average settles on one number, the instantaneous speed, and that limit is the derivative|At a steady speed distance grows along a straight line, and the reading is its slope|At a sudden impact the speed just before and just after differ, so there is no single speed at that instant: no derivative there"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the product rule from the definition of the derivative: if f and g are differentiable at a, then (fg)'(a) = f'(a) g(a) + f(a) g'(a)." key_points="Writes the difference quotient (f(a+h) g(a+h) - f(a) g(a)) / h|Adds and subtracts f(a+h) g(a) to split it into f(a+h) (g(a+h) - g(a))/h + g(a) (f(a+h) - f(a))/h|Uses that the two difference quotients tend to g'(a) and f'(a)|Uses that f is continuous at a because it is differentiable there, so f(a+h) tends to f(a)|Concludes by the limit laws that the limit is f(a) g'(a) + g(a) f'(a)"}
:::
