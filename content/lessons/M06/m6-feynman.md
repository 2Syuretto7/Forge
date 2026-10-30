# Explain it plainly: why logarithms turn multiplying into adding

Explain to a 12-year-old what a logarithm is, why it turns multiplication into addition, and why that is useful when you multiply many probabilities.

Guidelines:

- Write 150 to 400 words.
- Start from counting zeros, or from doubling, not from a definition.
- Use one example with real numbers, and one with probabilities (rolling dice, flipping coins, or guessing letters).
- Say what would go wrong without logarithms.

:::feynman{id=f1 prompt="Explain why a logarithm turns multiplication into addition, and why that is useful for probabilities." key_points="A logarithm is an exponent: it counts how many times you multiply the base to reach a number, like counting zeros for powers of ten|Multiplying two numbers adds their exponents, so the logarithm of a product is the sum of the logarithms|The probability that many independent things all happen is the product of their probabilities, which shrinks very fast|Such products become too small for a computer to store and turn into zero, while the sum of their logarithms stays a modest number|So models add log-probabilities instead of multiplying probabilities, and compare them on a log scale"}
:::
