# Scale it: forgetting, packing and storing teachers

## Forgetting

:::exercise{ref=e08}
:::

## Packing

:::exercise{ref=e09}
:::

## Teachers at scale

::::predict{id=p3 kind=choice answer=c}
You distill a teacher with a vocabulary of 50,000 tokens over a corpus of 10 billion tokens, storing the teacher's probabilities as 16-bit numbers. Storing the full distributions would take about:

- 1 GB.
- 100 GB.
- 1 PB (a million GB).
- 1 TB.

:::reveal
$10^{10} \times 5 \times 10^4 \times 2$ bytes $= 10^{15}$ bytes: a petabyte. Keeping only the top few probabilities per token (exercise 10), or distilling online with the teacher running next to the student, are the practical options.
:::
::::

:::exercise{ref=e10}
:::
