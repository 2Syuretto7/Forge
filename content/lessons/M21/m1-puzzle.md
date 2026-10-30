# Puzzle: a positive test

A test is 99 percent accurate: it is positive for 99 percent of ill people and negative for 99 percent of healthy ones. The disease affects 1 person in 1,000. You test positive.

::::predict{id=p1 kind=numeric answer=9 tol=1}
What is the probability, in percent, that you are ill?

:::reveal
About 9 percent. In 100,000 people, 100 are ill and 99 of them test positive; of the 99,900 healthy, 1 percent, 999, also test positive. So 99 of 1,098 positives are ill: 9.0 percent. The test is accurate, but the healthy outnumber the ill so heavily that its small error rate produces ten false alarms for every true case.
:::
::::

::::predict{id=p2 kind=choice answer=c}
You take a second, independent test, and it is positive again. What now?

- Still about 9 percent: a second test adds nothing.
- 99 percent: the test's accuracy.
- About 91 percent: the first posterior becomes the new prior.
- 100 percent.

:::reveal
About 91 percent. After the first positive the odds of illness are $99 : 999$; a second positive multiplies them by $99 : 1$, giving $9801 : 999$, about $91$ percent. This relies on the tests being independent given the disease status; two runs of the same flawed test are not, and the second adds less.
:::
::::

Each square is a person: ill and positive, ill and negative, healthy and positive. The posterior is the ill share of the positives. Raise the prevalence and watch the false alarms lose their majority; tick the box to test the positives again.

:::widget{name=BayesGrid prevalence=1 sensitivity=99 specificity=99}
:::

## Questions to carry into the derivation

1. What rules must any assignment of probabilities obey?
2. How does learning that an event happened change the probability of another?
3. How do you turn $P(\text{positive} \mid \text{ill})$ into $P(\text{ill} \mid \text{positive})$?
4. When is it safe to multiply probabilities?
