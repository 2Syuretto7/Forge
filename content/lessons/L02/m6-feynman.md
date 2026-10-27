# Explain it plainly: maximum likelihood and its uncertainty

Explain maximum likelihood to a smart friend who has never heard the term. Use the coin as your running example, then say what the estimate does not tell you and how you would measure that.

- Write 150 to 400 words.
- Give a concrete example with numbers.
- Explain why maximizing the likelihood is a reasonable thing to do, not only how.
- If you use the words "likelihood", "prior" or "bootstrap", say what they mean in plain language.

:::feynman{id=f1 prompt="Explain what maximum likelihood estimation does, using a coin as the example, and explain how much you should trust the estimate after a few flips versus many flips." key_points="The likelihood scores each possible parameter by how probable it makes the observed data|The maximum likelihood estimate for a coin is the observed fraction of heads|Uncertainty shrinks like one over the square root of the number of flips|With very few flips the estimate can be extreme, such as zero, and a prior or smoothing pulls it toward plausible values|The bootstrap or the curvature of the log-likelihood quantifies how much the estimate would change with new data"}
:::
