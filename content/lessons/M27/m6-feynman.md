# Explain it plainly: entropy as questions

Explain why entropy is the average number of yes-or-no questions.

Guidelines:

- Write 150 to 400 words.
- Use a small example: a fair die, or four outcomes with probabilities one half, one quarter, one eighth and one eighth.
- Say how the best questions depend on the probabilities.
- Say what changes when the probabilities are not powers of one half, and how a cross-entropy fits the same picture.

:::feynman{id=f1 prompt="Explain why entropy is the average number of yes-or-no questions." key_points="A yes-or-no question has two answers, so each answer can carry at most one bit, and the best questions split the remaining probability in half|An outcome of probability p needs about log2(1/p) such questions, its surprisal, so likely outcomes are reached in few questions and rare ones in many|Averaging over outcomes gives the entropy, the sum of p log2(1/p), as the average number of questions for the best strategy|A strategy of questions is a prefix code, and Shannon's theorem says no prefix code averages fewer than H bits and the best come within one|Asking the questions that would be best for a wrong model q costs the cross-entropy H(p, q) on average, and the excess is the KL divergence"}
:::

## A written proof

:::feynman{id=proof1 prompt="Let p-hat be the empirical distribution of categorical data. Prove that maximizing the average log-likelihood of a model q is equivalent to minimizing KL(p-hat || q), and that the maximizer is q = p-hat." key_points="Rewrites the average log-likelihood (1/n) sum_i log q(x_i) as sum_x p-hat(x) log q(x) by grouping equal observations|Recognizes minus that sum as the cross-entropy H(p-hat, q)|Splits the cross-entropy as H(p-hat) + KL(p-hat || q), where H(p-hat) does not depend on q|Concludes that maximizing likelihood minimizes KL(p-hat || q)|Uses Gibbs' inequality, KL >= 0 with equality only at q = p-hat, to identify the maximizer"}
:::
