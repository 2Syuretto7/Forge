# Break it: summation order and rearrangement

On paper, addition is commutative and associative: order never matters. In floating point it does, and for infinite series, even on paper, it can.

## The order of summation

Adding $\sum 1/k^2$ for $k$ up to a million in 32-bit floats, once from the big terms down and once from the small terms up.

::::predict{id=p5 kind=choice answer=b}
Which order gives the more accurate sum in 32-bit floating point?

- Largest terms first: the important terms go in while the total is small.
- Smallest terms first: tiny terms are added to each other before they meet a large total that would swallow them.
- Neither: addition is commutative.

:::reveal
Smallest first. A float32 keeps about 7 significant digits. Once the running total is near 1.64, adding $10^{-12}$ changes nothing: the term is below the total's last digit and vanishes. Adding the tiny terms to each other first lets them accumulate into something big enough to count. The backward sum is accurate to about $10^{-7}$; the forward one loses about $2 \times 10^{-4}$, and you will measure both.
:::
::::

:::exercise{ref=e13}
:::

## Rearranging a series

The alternating harmonic series $1 - \frac{1}{2} + \frac{1}{3} - \frac{1}{4} + \dots$ converges to $\ln 2 \approx 0.693$. Reorder the same terms as one positive and two negatives at a time, $1 - \frac{1}{2} - \frac{1}{4} + \frac{1}{3} - \frac{1}{6} - \frac{1}{8} + \dots$, and it converges to half that. Bernhard Riemann proved more: reorder it cleverly and it converges to any number you like. Commutativity holds for finite sums, not infinite ones.

:::widget{name=SeriesStacker series=alternating logn=3}
:::

:::exercise{ref=e14}
:::

## Induction with a broken part

:::exercise{ref=e15}
:::

## What to take away

- In floating point, add small numbers first, or use a smarter method (M26 builds compensated summation).
- An infinite series is a limit; rearranging its terms can change the limit unless the series converges absolutely.
- Induction needs both parts. A step without a base proves nothing; a base without a step proves one case.
