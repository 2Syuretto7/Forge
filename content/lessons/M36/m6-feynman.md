# Explain it plainly: nudging the odds

Explain how you can improve a choice you cannot differentiate by nudging the odds of the good outcomes.

Guidelines:

- Write 150 to 400 words.
- Use a model choosing among a few answers, with a score for each, as the example.
- Say why the method is unbiased and why it is noisy.
- Say what a baseline does.

:::feynman{id=f1 prompt="Explain how you can improve a choice you cannot differentiate by nudging the odds of the good outcomes." key_points="The expected reward depends smoothly on the probabilities of the choices even though each sampled choice is discrete|Its gradient equals the average of the reward times the gradient of the log-probability of the sampled choice, so samples estimate it without bias|Each update raises the probability of what was sampled in proportion to its reward, so better outcomes gain probability faster than worse ones|The estimate is noisy because it learns only from sampled outcomes, and rewards far from zero push every sampled choice up or down|Subtracting a baseline that does not depend on the choice, such as the average reward, keeps the estimate unbiased and removes most of that noise"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that the REINFORCE estimator with a constant baseline, (r_a - b) grad log pi_a with a sampled from pi, is an unbiased estimate of the gradient of the expected reward sum_a pi_a r_a." key_points="Writes the gradient of the expected reward as sum_a r_a grad pi_a|Uses grad pi_a = pi_a grad log pi_a to rewrite it as the expectation of r_a grad log pi_a under pi|Shows that the expected score is zero: sum_a pi_a grad log pi_a = grad sum_a pi_a = grad 1 = 0|Concludes that the expectation of b grad log pi_a is b times zero for a baseline independent of a|Combines the two to show the expectation of (r_a - b) grad log pi_a equals the gradient"}
:::
