# Confusing the conditionals

- `naive_reading(sensitivity)`: the mistaken answer "the probability of illness after a positive test is the sensitivity".
- `correct(prevalence, sensitivity, specificity)`: $P(\text{ill} \mid +)$.
- `overstatement(prevalence, sensitivity, specificity)`: the ratio of the naive reading to the correct value.
- `prosecutor(match_prob, population)`: a DNA profile matches 1 in a million people at random; in a city of `population` people with one guilty person, the probability that a matching suspect, found by searching the database of the whole city, is guilty: $1/(1 + \text{match\_prob} \times (\text{population} - 1))$.

## Hints

1. Bayes' rule as in e02.
2. The ratio grows as the prevalence falls.
3. In a city of 5 million, about 5 innocent people match besides the guilty one.
