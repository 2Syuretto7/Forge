# Explain it plainly: the winner's curse

Explain why checking many models against one test set makes the winner look better than it is.

Guidelines:

- Write 150 to 400 words.
- Use models that only guess as the example.
- Say how large the effect is and how it grows with the number of models.
- Say what fixes it.

:::feynman{id=f1 prompt="Explain why checking many models against one test set makes the winner look better than it is." key_points="Each model's test score is its true accuracy plus random noise from the finite test set, of size about 1 over the square root of n|Choosing the best score chooses the model whose noise happened to be largest, so the winner's score is biased upward|The bias grows with the number of models, roughly like the square root of the log of the number of models in standard errors|A single-model interval no longer covers the truth for the selected model; the union bound widens it by counting every model compared|A fresh test set used only once after selection gives an unbiased estimate"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the finite-class bound: if H has k hypotheses with losses in [0, 1] and the n test examples are independent, then with probability at least 1 - delta every h in H has |R_hat(h) - R(h)| < sqrt(ln(2k/delta) / (2n))." key_points="For a single fixed h, applies Hoeffding's inequality to the n independent losses to get P(|R_hat(h) - R(h)| >= eps) <= 2 exp(-2 n eps^2)|Notes that the failure event for the class is the union of the failure events of the k hypotheses|Applies the union bound to get a probability at most 2k exp(-2 n eps^2)|Sets 2k exp(-2 n eps^2) = delta and solves for eps = sqrt(ln(2k/delta) / (2n))|Concludes that the complementary event, every h within eps, has probability at least 1 - delta, and so it covers whichever h is selected"}
:::
