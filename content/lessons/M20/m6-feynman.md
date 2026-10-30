# Explain it plainly: stretching thins probability

Explain why stretching space thins out probability.

Guidelines:

- Write 150 to 400 words.
- Use sand spread on a rubber sheet as the picture.
- Say what is conserved and what changes.
- Say what the Jacobian determinant measures in the picture.

:::feynman{id=f1 prompt="Explain why stretching space thins out probability." key_points="Probability behaves like a fixed amount of sand spread over the space|A map moves the sand around without creating or destroying any|Where the map stretches a small region to twice its area, the same sand covers twice the area, so its density halves|The Jacobian determinant measures how much the map stretches area locally|So the new density is the old density divided by the absolute value of the Jacobian determinant"}
:::

## A written proof

:::feynman{id=proof1 prompt="Prove the change-of-variables formula for densities in one dimension: if X has density p_X and Y = g(X) with g increasing and differentiable, then p_Y(y) = p_X(g^{-1}(y)) / g'(g^{-1}(y)); say what changes when g is decreasing." key_points="Writes the distribution function of Y as P(Y <= y) = P(X <= g^{-1}(y)) = F_X(g^{-1}(y)) for increasing g|Differentiates with the chain rule to get p_Y(y) = p_X(g^{-1}(y)) times the derivative of g^{-1} at y|Uses the inverse function rule (g^{-1})'(y) = 1 / g'(g^{-1}(y))|For decreasing g, uses P(Y <= y) = 1 - F_X(g^{-1}(y)), which flips the sign of the derivative|Concludes p_Y(y) = p_X(g^{-1}(y)) / |g'(g^{-1}(y))| in both cases"}
:::
