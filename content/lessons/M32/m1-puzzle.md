# Puzzle: how many shuffles?

A riffle shuffle cuts the deck roughly in half and interleaves the halves by letting cards drop from each hand. Each shuffle depends only on the current order of the deck, not on how it got there.

::::predict{id=p1 kind=numeric answer=7 tol=1}
How many riffle shuffles until a 52-card deck is closer to random than not, meaning that the total variation distance from the uniform distribution over all $52!$ orders falls below one half?

:::reveal
Seven. Bayer and Diaconis computed the distance exactly: after 5 shuffles it is $0.924$, after 6 $0.614$, after 7 $0.334$, after 8 $0.167$. For the first four shuffles it is $1.000$ to three places, and then it collapses in a few steps. You will reproduce the table in e05.
:::
::::

::::predict{id=p2 kind=choice answer=c}
After 7 shuffles the distance is $0.334$. What is it after 14?

- About $0.167$, half as much.
- About $0.08$.
- About $0.003$.
- Exactly 0.

:::reveal
About $0.003$ (precisely $0.0027$). Past the drop, each further shuffle halves the distance, so seven more shuffles divide it by about $2^7$. It never reaches exactly 0: some orders remain slightly more likely than others for ever. The rate of halving is the second eigenvalue of the shuffle's transition matrix at work, the subject of Section 4.
:::
::::

## Questions to carry into the derivation

1. What is the distribution a chain settles into, and when is it unique?
2. How fast does it settle, and what number controls the speed?
3. How do you build a chain that settles into a distribution of your choosing?
4. How many independent samples is a correlated chain worth?
