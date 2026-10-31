# Explain it plainly: the lying straight line

Explain why a straight line on a log-log plot can still be a lie at larger scale.

Guidelines:

- Write 150 to 400 words.
- Use a loss curve with an irreducible floor as the example.
- Say what the error bars of the fit do and do not measure.
- Say what you would do before betting on the forecast.

:::feynman{id=f1 prompt="Explain why a straight line on a log-log plot can still be a lie at larger scale." key_points="Loss curves typically have an irreducible floor, so the true curve bends toward a horizontal line on log-log axes|Over a limited range the bend is gentle, so a straight line fits with a high R^2 while its slope is too shallow|Extrapolated, the straight line keeps falling and eventually predicts losses below the floor, which is impossible|The fit's error bars measure noise in the parameters given the model, not whether the model's form holds beyond the data, and the law itself can change beyond the data|The remedies are to fit the floor, extrapolate as little as possible, use honest intervals for few runs, and check with a run closer to the target scale"}
:::

## A written proof

:::feynman{id=proof1 prompt="Derive the compute-optimal allocation: minimize L(N, D) = E + A N^(-alpha) + B D^(-beta) subject to 6 N D = C, and show that N_opt is proportional to C^(beta / (alpha + beta))." key_points="Substitutes D = C / (6 N) to obtain a function of N alone|Differentiates in N and sets the derivative to zero: -alpha A N^(-alpha - 1) + beta B (C/6)^(-beta) N^(beta - 1) = 0|Solves for N to get N^(alpha + beta) = (alpha A / (beta B)) (C/6)^beta|Concludes N_opt = (alpha A / (beta B))^(1/(alpha + beta)) (C/6)^(beta/(alpha + beta)), and D_opt proportional to C^(alpha/(alpha + beta))|Checks that the stationary point is a minimum, since the loss tends to infinity as N tends to 0 or to C/6"}
:::
