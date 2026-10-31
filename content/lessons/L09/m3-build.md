# Build: attention from scratch in NumPy

## The softmax and one head

:::exercise{ref=e01}
:::

:::exercise{ref=e02}
:::

:::exercise{ref=e03}
:::

## Many heads

:::exercise{ref=e04}
:::

:::exercise{ref=e05}
:::

## Positions

:::exercise{ref=e06}
:::

::::predict{id=p3 kind=choice answer=a}
You apply RoPE to the queries and keys of a sentence, then shift every position by 100 (the same sentence starting later in a document). What happens to the attention weights?

- They are unchanged: every query-key score depends only on the difference of positions.
- They change a little, because the rotations are larger.
- They become uniform.
- The scores for distant pairs grow.

:::reveal
Each score is $q^\top R((n - m)\theta) k$, and shifting both positions by 100 leaves $n - m$ unchanged, so every score, and every weight, is exactly the same. Learned absolute position embeddings have no such guarantee.
:::
::::

:::exercise{ref=e07}
:::

## The block

:::exercise{ref=e08}
:::
