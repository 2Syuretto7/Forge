# Scale: a thousand dimensions and condition numbers up to 100,000

Gradient descent does not care about the dimension; it cares about the spread of the eigenvalues. Here the dimension is 1,000 and the condition number climbs from 10 to $10^5$.

::::predict{id=p4 kind=choice answer=a}
With the best fixed step, gradient descent needs about 6,900 iterations at $\kappa = 1000$ for a relative error of $10^{-6}$. About how many at $\kappa = 10^5$?

- About 690,000
- About 69,000
- About 21,000, growing like $\sqrt\kappa$
- About 6,900: the dimension did not change

:::reveal
About 690,000: the count grows in proportion to $\kappa$. At that point you predict rather than run: the eigenvalues alone fix the error after $k$ steps, and the prediction can be checked exactly where running is affordable. Rescaling (e12) or momentum (M29) is how practice avoids such counts.
:::
::::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
