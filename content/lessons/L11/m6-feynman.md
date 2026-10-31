# Explain it plainly: spending a compute budget

Explain to an engineering manager how to decide the model size and the amount of training data for a fixed compute budget.

- Write 150 to 400 words.
- Use the relation between compute, parameters and tokens.
- Explain why both should grow with the budget, and roughly how fast.
- Mention one way such a plan can mislead, and how to check it.

:::feynman{id=f1 prompt="Explain how to choose the model size and the number of training tokens for a fixed compute budget, using scaling laws, and describe one way such predictions can mislead." key_points="Training compute is about 6 times parameters times tokens, so a budget trades model size against data|The loss falls as a power law in parameters and in tokens toward an irreducible floor|At the optimum the marginal benefits balance, so parameters and tokens both grow with the budget, roughly as its square root, about 20 tokens per parameter|Fits are made on small runs and extrapolated, so they should be checked on a held-out larger run and reported with uncertainty|Fitting too narrow a range, ignoring the floor or not retuning the learning rate per size biases the predictions"}
:::
