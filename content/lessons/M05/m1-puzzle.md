# Puzzle: adding forever

Add $1 + \frac{1}{2} + \frac{1}{4} + \frac{1}{8} + \dots$ forever. Then add $1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4} + \dots$ forever.

Both lists of terms shrink toward zero. Both sums go on without end.

::::predict{id=p1 kind=choice answer=a}
Which of the two infinite sums is a finite number?

- Only $1 + \frac{1}{2} + \frac{1}{4} + \dots$
- Only $1 + \frac{1}{2} + \frac{1}{3} + \dots$
- Both: the terms shrink to zero.
- Neither: adding forever always gives infinity.

:::reveal
Only the first. Its sums are $1, 1.5, 1.75, 1.875, \dots$, each halfway from the previous one to 2, and they settle at exactly 2. The second, the **harmonic series**, grows without limit, but so slowly that after a million terms it has only reached about 14.4. Shrinking terms are necessary for a finite sum but not enough: they must shrink fast enough.
:::
::::

::::predict{id=p2 kind=numeric answer=14.4 tol=1.5}
Estimate $1 + \frac{1}{2} + \frac{1}{3} + \dots + \frac{1}{1{,}000{,}000}$.

:::reveal
About 14.39. The sum of the first $n$ terms is close to $\ln n + 0.5772$, and $\ln(10^6) \approx 13.8$. Ten times more terms adds only $\ln 10 \approx 2.3$. To pass 10 you need 12,367 terms; to pass 100 you would need about $10^{43}$.
:::
::::

Watch both in the widget: set the geometric series with ratio 0.5, then switch to the harmonic series, open the logarithmic axis, and push the number of terms to a million.

:::widget{name=SeriesStacker series=geometric r=0.5 logn=1.5}
:::

## Questions to carry into the derivation

1. What does it mean, exactly, for a sequence to "settle" on a value?
2. Is there a formula for $1 + r + r^2 + \dots + r^{n-1}$?
3. How can you prove a formula for every $n$ at once?
4. Why does the harmonic series diverge, and how fast?
