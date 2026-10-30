# Scale: 20,000 documents and a reliability diagram

Train naive Bayes on 16,000 synthetic messages and test it on 4,000. It classifies well; then check whether its probabilities mean what they say.

::::predict{id=p4 kind=choice answer=a}
Naive Bayes counts each word of a phrase as independent evidence. How do you expect its predicted probabilities to compare with the observed frequencies?

- Too extreme: among messages it calls 99 percent spam, fewer than 99 percent are.
- Too timid: they cluster near 50 percent.
- Exactly right: Bayes' rule is exact.
- Random: no relation to the frequencies.

:::reveal
Too extreme. Counting correlated evidence several times pushes the log-odds too far, so the probabilities sit too close to 0 and 1. The reliability diagram shows it, and a temperature fitted on held-out data, here near 2, pulls them back.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

M08's counting tree, read as probability: each path is an equally likely outcome, and conditioning on the first choice keeps only the paths that start with it, so the probability of a path is the product of the shares along it.

:::widget{name=CountingTree n=2 k=2}
:::
