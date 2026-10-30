# Bayes' rule over discrete hypotheses

For a finite set of hypotheses:

- `posterior(prior, likelihood)`: both arrays of shape `(H,)`; return the normalized posterior.
- `positive_test_posterior(prevalence, sensitivity, false_positive_rate)`: the probability of the condition given one positive test.
- `sequential(prior, likelihoods)`: `likelihoods` has shape `(T, H)`, one row per independent observation; apply Bayes' rule once per row and return the final posterior.

## Hints

1. Multiply, then divide by the sum.
2. For the test, use two hypotheses: condition, no condition.
3. Applying the update row by row equals one update with the product of the rows.
