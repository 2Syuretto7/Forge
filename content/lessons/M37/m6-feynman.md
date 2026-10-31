# Explain it plainly: following the score home

Explain how knowing which way density increases lets you turn noise back into data.

Guidelines:

- Write 150 to 400 words.
- Use a target with two clusters as the example.
- Say what the forward process does and why it ends at a Gaussian.
- Say what is learned and how.

:::feynman{id=f1 prompt="Explain how knowing which way density increases lets you turn noise back into data." key_points="The forward process shrinks the data toward zero and adds Gaussian noise until its distribution is a standard Gaussian, which is easy to sample|The score, the gradient of the log density of the noised data at each noise level, points toward where noised data are more likely|The reverse-time process starts from Gaussian noise and at each step moves along the score and adds a little fresh noise, so its distribution at each time matches the noised data's|At the end of the reverse process the samples are distributed as the data, new points rather than copies|The score is learned from samples by denoising score matching: predict the added noise from the noised point, at every noise level"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that the denoising score-matching objective E || s(x_t) + eps / sigma ||^2, with x_t = a x_0 + sigma eps, is minimized over all functions s by the score of the marginal density p_t." key_points="Notes that -eps / sigma equals the conditional score, the gradient in x_t of log p(x_t | x_0) for the Gaussian conditional|Uses that a squared error E || s(x_t) - Y ||^2 is minimized over functions of x_t by the conditional expectation E[Y | x_t]|Writes the marginal score as grad p_t / p_t with p_t(x) = integral p(x | x_0) p(x_0) dx_0, and moves the gradient inside the integral|Shows that grad p_t(x) / p_t(x) = integral grad log p(x | x_0) p(x_0 | x) dx_0, the conditional expectation of the conditional score|Concludes that the minimizer is the marginal score grad log p_t"}
:::
