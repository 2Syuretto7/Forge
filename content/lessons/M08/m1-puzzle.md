# Puzzle: twenty-three people

A room holds 23 people. Ignore leap years and assume every birthday is equally likely and independent of the others.

::::predict{id=p1 kind=choice answer=a}
Is it more likely than not that two of them share a birthday?

- More likely than not.
- Less likely than not: 23 is far fewer than 365.
- About as likely as not, exactly 50 percent.

:::reveal
More likely: about 50.7 percent. Most people guess low because they think about whether someone shares **their** birthday (23 chances in 365, about 6 percent). The question is about any pair, and 23 people make many pairs.
:::
::::

::::predict{id=p2 kind=numeric answer=253 tol=0.5}
How many different pairs of people are there among 23?

:::reveal
$23 \times 22 / 2 = 253$. Each person pairs with 22 others, and each pair is counted twice that way. With 253 pairs each matching with probability $1/365$, about $253/365 \approx 0.69$ matches are expected, so a match being likely is no longer a surprise. The exact probability takes a little more care, because the pairs are not independent; you will derive it.
:::
::::

The widget plots the chance of a shared birthday against the number of people. Find where it crosses one half, and how fast it rises after that.

:::widget{name=CountingTree mode=birthday m=23}
:::

## Questions to carry into the derivation

1. How do you count arrangements and selections without listing them?
2. What are binomial coefficients, and why does Pascal's triangle compute them?
3. What is a probability, when outcomes are equally likely?
4. How do you compute the chance that "at least one" thing happens?
