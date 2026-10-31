# Build: three models, three solvers

Nine exercises take you from the closed-form least-squares solution to a full softmax classifier with honest evaluation. Three of them check gradients against finite differences.

## Linear regression

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

## Logistic regression

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

::::predict{id=p3 kind=numeric answer=0 tol=0.05}
You fit logistic regression with an intercept to a dataset where 30 percent of the labels are 1, using features that carry no information at all. After training to convergence, what is the average of the predicted probabilities minus 0.3?

:::reveal
At the optimum the gradient with respect to the intercept is zero, and that gradient is the mean of $\sigma(a_i) - y_i$. So the predicted probabilities average exactly to the observed rate of 1s, $0.3$, and the difference is $0$. This "mean matching" holds for any logistic regression with an intercept, informative features or not.
:::
::::

## Softmax regression and the pipeline around it

:::exercise{ref=e06}
:::

:::exercise{ref=e07}
:::

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::
