# Recall bridge: from one step to a whole run

M28 showed that gradient descent on a quadratic needs a number of steps proportional to the condition number, and that the step must stay below $2/L$. This lesson proves those rates for general smooth functions, beats them with momentum, and then confronts what real training adds: gradients that are only noisy estimates, computed from a minibatch, and the adaptive optimizer that nearly everyone uses. Clear your due cards above first.

:::edge{from=M28 text="the condition number and the step-size limit"}
:::

:::edge{from=M24 text="the variance of an average, now of minibatch gradients"}
:::

:::edge{from=M13 text="eigenvalues of the Hessian set the best momentum"}
:::

## What carries over

From M28, the error of gradient descent along an eigenvector of the Hessian is multiplied by $1 - \eta\lambda$ each step. From M24, an average of $B$ independent terms has variance $\sigma^2/B$. From M05, an error multiplied by $\rho$ each step reaches $\varepsilon$ in about $\log(1/\varepsilon)/\log(1/\rho)$ steps.
