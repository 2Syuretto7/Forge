# Explain it plainly: cross-entropy and KL divergence

A colleague sees "validation loss 1.5 nats" on a dashboard and asks what it means and whether it could reach zero. Explain cross-entropy and KL divergence to them, using a concrete example with a coin or a die.

- Write 150 to 400 words.
- Give a numerical example.
- Explain why the loss cannot go below the entropy of the data, and what the gap means.
- Explain what the unit "nats" means.

:::feynman{id=f1 prompt="Explain what a cross-entropy loss measures, what KL divergence is, why the loss cannot fall below the entropy of the data, and what 1.5 nats per token means in plain terms." key_points="Surprise is minus the log of the probability given to what actually happened|Cross-entropy is the model's average surprise on data from the true distribution|Entropy is the unavoidable surprise of the data itself, so cross-entropy is at least the entropy|KL divergence is the gap between cross-entropy and entropy, is never negative, and is zero only for a perfect model|1.5 nats means the model gives about e to the minus 1.5, roughly 0.22, to the correct token on average, like choosing among about 4.5 options"}
:::
