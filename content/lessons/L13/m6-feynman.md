# Explain it plainly: how attention works

Explain to a programmer who knows what a dictionary lookup is how a transformer's attention layer decides which earlier words to use when processing a word.

- Write 150 to 400 words.
- Use a concrete sentence as the example.
- Explain queries, keys and values, the softmax, and why the scores are scaled.
- Mention why the model needs position information or a causal mask.

:::feynman{id=f1 prompt="Explain how an attention layer lets each word gather information from other words, using queries, keys and values, and explain the scaling of the scores and the role of positions or the causal mask." key_points="Each position produces a query, and every position a key and a value, through learned projections|Scores are dot products of the query with every key, turned into weights by a softmax, and the output is the weighted average of the values|Scores are divided by the square root of the dimension so the softmax does not saturate and gradients keep flowing|Attention alone ignores word order, so positional information must be added|A causal mask stops each position from seeing later positions, so all next-token predictions train in one pass"}
:::
