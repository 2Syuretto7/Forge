# Scale: gradients in 10,000 dimensions

A function of $n = 10{,}000$ inputs. Its analytic gradient costs about as much as one evaluation; central differences cost $2n = 20{,}000$ evaluations.

::::predict{id=p4 kind=choice answer=c}
An evaluation takes 1 ms. How long does a central-difference gradient take for $10^4$ inputs, and for a model with $10^8$ parameters?

- 20 ms and 200 ms.
- 2 s and 20 s.
- 20 s and about 2.3 days.
- Under a second for both: the computer is fast.

:::reveal
$2 \times 10^4 \times 1\,\text{ms} = 20$ s, and $2 \times 10^8$ ms $\approx 2.3$ days, for one gradient. Training takes millions of gradients. Finite differences are a test, never a training method; a random-direction check (e11) tests a huge gradient in a few evaluations.
:::
::::

:::exercise{ref=e10}
:::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::
