# Break it: wrong order, overflow and added probabilities

Counting mistakes are rarely arithmetic. They are mismatches: order counted on top and not on the bottom, probabilities added that overlap, numbers computed in a type that cannot hold them.

## Ordered on top, unordered below

Two cards are drawn from a deck. The chance both are aces is $\binom{4}{2} / \binom{52}{2} = 6/1326 = 1/221$. Counting the favourable outcomes in order ($4 \times 3 = 12$) but the possible outcomes without order ($\binom{52}{2}$) doubles the answer.

:::exercise{ref=e13}
:::

## 200 choose 100 with factorials

::::predict{id=p5 kind=choice answer=b}
You compute $\binom{200}{100}$ as `factorial(200) / (factorial(100) * factorial(100))` with the factorials converted to 64-bit floats. What happens?

- It works: the answer, about $9 \times 10^{58}$, is far below the float limit of $1.8 \times 10^{308}$.
- It fails: $200!$ is about $8 \times 10^{374}$, above the float limit, even though the final answer is not.
- It works but loses half the digits.

:::reveal
$200! \approx 7.9 \times 10^{374}$ overflows before the division can bring the result back down; floats top out around $1.8 \times 10^{308}$, and $171!$ already exceeds that. The fix is to never form the giant intermediate: multiply and divide step by step, use exact integers, or add logarithms with the log-gamma function and exponentiate at the end.
:::
::::

:::exercise{ref=e14}
:::

## Adding probabilities that overlap

A seventeenth-century gambler, the Chevalier de Méré, reasoned that one six in four rolls of a die has probability $4 \times \frac{1}{6} = \frac{2}{3}$. The same reasoning gives 7 rolls a probability of $\frac{7}{6}$, which is impossible.

:::exercise{ref=e15}
:::

## What to take away

- Decide whether order matters, and count the favourable and the possible outcomes the same way.
- Never form a huge intermediate in floating point; cancel as you go or work with logarithms.
- Add probabilities only for disjoint events. For "at least one", use the complement.
