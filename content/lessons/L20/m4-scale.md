# Scale it: serving, evaluation and an auditable pipeline

:::exercise{ref=e08}
:::

:::exercise{ref=e09}
:::

::::predict{id=p3 kind=numeric answer=0.3 tol=0.01}
A model solves a problem in 3 of 10 samples. What is its estimated pass@1?

:::reveal
$1 - \binom{7}{1}/\binom{10}{1} = 0.3$: the fraction correct. pass@2 is $1 - \binom{7}{2}/\binom{10}{2} = 1 - 21/45 \approx 0.53$, more than $1 - 0.7^2 = 0.51$ because the two samples are drawn without replacement from the ten. Report the $k$ that matches how the model will be used.
:::
::::

:::exercise{ref=e10}
:::
