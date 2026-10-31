# Explain it plainly: the price of a constraint

Explain what a Lagrange multiplier is as the price of a constraint.

Guidelines:

- Write 150 to 400 words.
- Use a budget: a limited amount of something you would like more of.
- Say what the multiplier is when the budget is not fully used.
- Say what the multipliers of the softmax problem price.

:::feynman{id=f1 prompt="Explain what a Lagrange multiplier is as the price of a constraint." key_points="The Lagrangian charges each constraint's violation at a rate, the multiplier|At the optimum the multiplier equals how much the optimal value would improve per unit of relaxation of the constraint|A constraint that is not binding at the optimum can be relaxed without changing anything, so its price is zero: complementary slackness|For inequality constraints the price is never negative, since relaxing a constraint can only help|In the entropy-regularized reward problem the temperature prices certainty and the normalization multiplier fixes the total probability, which together produce softmax"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove that the maximizer of sum_i p_i r_i - beta KL(p || pi) over probability distributions p, with all pi_i > 0, is p_i = pi_i exp(r_i / beta) / Z." key_points="Writes the objective as sum p_i r_i - beta sum p_i log(p_i / pi_i), a concave function of p|Adds a multiplier nu for the constraint sum p_i = 1 and sets the derivative r_i - beta (log(p_i / pi_i) + 1) - nu to zero|Solves to get log(p_i / pi_i) = r_i / beta + constant, so p_i is proportional to pi_i exp(r_i / beta)|Fixes the constant by normalization, giving the division by Z = sum_j pi_j exp(r_j / beta)|Notes the solution has every p_i > 0, so the constraints p_i >= 0 are inactive, and concavity makes the stationary point the maximum"}
:::
