# Puzzle: two random directions

Pick two directions at random in 4,096 dimensions, the width of a large language model's hidden state: two vectors with independent standard normal entries.

::::predict{id=p1 kind=numeric answer=90 tol=2}
What is the angle between them, in degrees?

:::reveal
$90°$, almost exactly. In three dimensions the angle could be anything from $0°$ to $180°$; in 4,096 it is nearly always within a degree or two of a right angle.
:::
::::

::::predict{id=p2 kind=choice answer=b}
Over a million random pairs, how far from $90°$ is a typical angle?

- About $0.01°$.
- About $0.9°$.
- About $10°$.
- About $45°$.

:::reveal
About $0.9°$: the cosine has standard deviation $1/\sqrt{4096} = 1/64$, which is $0.9°$ in angle. Even the most extreme of a million pairs lands only about five standard deviations out, $4.5°$ from perpendicular. You will measure 2,000 pairs in e02.
:::
::::

## Questions to carry into the derivation

1. Why are random vectors all about the same length in high dimension?
2. Why are they nearly perpendicular, and what does that do to attention scores?
3. How few dimensions can hold $n$ points without distorting their distances?
4. What does the spectrum of a matrix of pure noise look like, and how does a real signal show up in it?
