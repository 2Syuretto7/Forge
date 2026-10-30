# Derivation: probability, conditioning and Bayes' rule

## 1. Sample spaces, events and the axioms

A **sample space** $\Omega$ is the set of possible outcomes; an **event** is a subset of it. A **probability** assigns each event $A$ a number $P(A)$ such that

1. $P(A) \geq 0$;
2. $P(\Omega) = 1$;
3. for disjoint events, $P(A \cup B) = P(A) + P(B)$ (and likewise for countably many).

Everything else follows: $P(A^c) = 1 - P(A)$, $P(\emptyset) = 0$, and **inclusion-exclusion** $P(A \cup B) = P(A) + P(B) - P(A \cap B)$, because the overlap would otherwise be counted twice. On a finite space with equally likely outcomes, $P(A) = |A|/|\Omega|$: M08's counting.

::::derivation{id=d1 title="Two dice"}
:::step
Roll two fair dice: 36 equally likely outcomes. The event "the sum is 7" contains 6 of them, so its probability is [[1/6]].
:::
:::step
"At least one six" is the complement of "no six", which has $25$ outcomes, so its probability is [[11/36]].
:::
::::

## 2. Conditional probability

Learning that $B$ happened shrinks the sample space to $B$. Probabilities within it are rescaled so that $B$ has probability 1:

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) > 0 .
$$

Rearranged, the **multiplication rule** $P(A \cap B) = P(A \mid B)\,P(B)$. Events are **independent** when learning one does not change the other: $P(A \mid B) = P(A)$, equivalently $P(A \cap B) = P(A)P(B)$.

::::derivation{id=d2 title="Conditioning on a die"}
:::step
Given that the sum of two dice is 7, the probability that the first die shows 6 is $P(\text{first} = 6 \text{ and sum} = 7)/P(\text{sum} = 7) = (1/36)/(6/36) =$ [[1/6]].
:::
:::step
That equals the unconditional $1/6$, so "first die is 6" and "sum is 7" are [[word:independent]], a coincidence of 7 being the middle sum: with "sum is 8" they are not.
:::
::::

## 3. Total probability and Bayes' rule

If $H_1, \dots, H_k$ are disjoint and cover $\Omega$ (hypotheses, exactly one true), any event $E$ splits into its parts:

$$
P(E) = \sum_i P(E \mid H_i)\,P(H_i) \qquad \text{(total probability)} .
$$

Writing $P(H_i \cap E)$ two ways, $P(H_i \mid E)P(E) = P(E \mid H_i)P(H_i)$, gives **Bayes' rule**:

$$
P(H_i \mid E) = \frac{P(E \mid H_i)\,P(H_i)}{\sum_j P(E \mid H_j)\,P(H_j)} .
$$

Prior times likelihood, renormalized. The area picture: draw the population as a square, split it by hypothesis (the prior), shade within each part the fraction that shows the evidence (the likelihood); the posterior is each part's share of the shaded area.

::::derivation{id=d3 title="The puzzle by Bayes' rule"}
:::step
$P(+) = 0.99 \times 0.001 + 0.01 \times 0.999 =$ [[0.01098|tol=0.00001]].
:::
:::step
$P(\text{ill} \mid +) = 0.00099 / 0.01098 \approx$ [[0.09|tol=0.002]].
:::
::::

**Odds form.** With two hypotheses, Bayes' rule is cleaner as odds: posterior odds = prior odds $\times$ likelihood ratio. For the test, prior odds $1 : 999$, likelihood ratio $0.99/0.01 = 99$, posterior odds $99 : 999$. Each independent piece of evidence multiplies the odds by its own ratio, and in logarithms the ratios add, which is how naive Bayes scores a document.

::::predict{id=p3 kind=choice answer=b}
A disease has prevalence 1 in 1,000, and a test has sensitivity 99 percent. What does "99 percent" tell you about $P(\text{ill} \mid +)$ on its own?

- It is 99 percent.
- Nothing, until you also know the false-positive rate and the base rate.
- It is at least 50 percent.
- It is 1 percent.

:::reveal
Nothing by itself. $P(+ \mid \text{ill}) = 0.99$ and $P(\text{ill} \mid +)$ are different conditional probabilities; confusing them is the **base-rate fallacy** (in courtrooms, the prosecutor's fallacy). With a specificity of 99.99 percent the posterior would be 91 percent; with 99 percent, 9 percent.
:::
::::

## 4. Conditional independence and naive Bayes

Events can be dependent and yet **independent given** a third: two tests both depend on the disease, so they are correlated in the population, but given the disease status their errors may be independent. Formally $P(A \cap B \mid C) = P(A \mid C)\,P(B \mid C)$.

**Naive Bayes** classifies a document by assuming its words are independent given the class:

$$
\log\frac{P(\text{spam} \mid \text{doc})}{P(\text{ham} \mid \text{doc})} = \log\frac{P(\text{spam})}{P(\text{ham})} + \sum_{\text{words } w} c_w \log\frac{P(w \mid \text{spam})}{P(w \mid \text{ham})},
$$

a sum of word scores weighted by counts $c_w$. Word probabilities are estimated from counts, with **Laplace smoothing** (add $\alpha$, usually 1, to every count) so that a word never seen in one class does not get probability 0 and veto everything else. The independence assumption is false (words come in phrases), so naive Bayes often classifies well while being **overconfident**: correlated words are counted as independent evidence, and its probabilities need calibration.

::::derivation{id=d4 title="Scoring with log-odds"}
:::step
A word appears with probability $0.02$ in spam and $0.005$ in ham. Each occurrence adds $\ln(0.02/0.005) = \ln 4 \approx$ [[1.386|tol=0.002]] to the log-odds.
:::
:::step
A phrase of two such words that always appear together is really one piece of evidence, but naive Bayes adds its score [[2]] times, doubling its weight.
:::
::::

## 5. Calibration

A classifier is **calibrated** when, among the cases it scores at 80 percent, about 80 percent are positive. A **reliability diagram** bins the predicted probabilities and plots each bin's average prediction against the observed frequency; the **expected calibration error** (ECE) is the average gap, weighted by bin size. An overconfident model sits below the diagonal at high predictions. **Temperature scaling** divides the log-odds by a constant $T > 1$, fitted on held-out data, which shrinks overconfident probabilities toward $\frac12$ without changing any decision.

::::derivation{id=d5 title="Temperature"}
:::step
A log-odds of $4$ means a probability of $1/(1 + e^{-4}) \approx 0.982$. With $T = 2$ it becomes $1/(1 + e^{-2}) \approx$ [[0.881|tol=0.001]].
:::
::::

:::edge{to=M22 text="random variables, distributions, expectation and variance."}
:::

:::edge{to=M27 text="surprise, -log P, and its average, the entropy."}
:::

## Summary

| Idea | Statement | Use |
| --- | --- | --- |
| Axioms | nonnegative, total 1, additive over disjoint events | consistent probabilities |
| Conditional | $P(A \mid B) = P(A \cap B)/P(B)$ | learning |
| Independence | $P(A \cap B) = P(A)P(B)$ | multiply only when true |
| Total probability | $P(E) = \sum_i P(E \mid H_i)P(H_i)$ | evidence from all causes |
| Bayes | posterior = prior $\times$ likelihood, renormalized | invert conditionals |
| Odds form | posterior odds = prior odds $\times$ likelihood ratio | sequential evidence |
| Naive Bayes | sum of log likelihood ratios, smoothed counts | text classification |
| Calibration | reliability diagram, ECE, temperature | trust the probabilities |
