# Explain it plainly: false alarms

Explain why most positive tests for a rare disease are false alarms.

Guidelines:

- Write 150 to 400 words.
- Use a town of 1,000 or 100,000 people as the picture.
- Count the true and the false positives.
- Say what would have to change for a positive result to be convincing.

:::feynman{id=f1 prompt="Explain why most positive tests for a rare disease are false alarms." key_points="Starts from a population and the base rate: very few people are ill|Counts the true positives: almost all of the few ill people|Counts the false positives: a small error rate applied to the many healthy people|Because the healthy are so many, false positives outnumber true ones, so a positive result is more likely a false alarm|A lower false-positive rate, a higher prior (symptoms, a risk group) or a second independent test makes a positive convincing"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove Bayes' rule with the law of total probability: if H1, ..., Hk are disjoint events covering the sample space with positive probabilities and P(E) > 0, then P(Hi | E) = P(E | Hi) P(Hi) / sum over j of P(E | Hj) P(Hj)." key_points="Writes P(Hi and E) two ways with the definition of conditional probability: P(Hi | E) P(E) and P(E | Hi) P(Hi)|Divides by P(E) to get P(Hi | E) = P(E | Hi) P(Hi) / P(E)|Splits E into the disjoint pieces E and Hj, which cover E because the Hj cover the sample space|Uses additivity and the multiplication rule to get P(E) = sum over j of P(E | Hj) P(Hj)|Substitutes to obtain the formula"}
:::
