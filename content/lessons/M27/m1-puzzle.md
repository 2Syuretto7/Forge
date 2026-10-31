# Puzzle: what does 1.5 nats mean?

A language model trained on English text reports a validation loss of **1.5 nats per character**. Another report on the same data says **2.16 bits per character**. A third says **perplexity 4.48**. Are these three models, or one?

::::predict{id=p1 kind=choice answer=d}
Which statement is right?

- Three different models: nats, bits and perplexity measure different things.
- Two models: nats and bits agree, perplexity is a different quantity.
- One model, but only if the vocabulary has exactly 4 characters.
- One model: they are the same number in three units.

:::reveal
All three describe the same average surprise. $1.5$ nats divided by $\ln 2 \approx 0.693$ is $2.16$ bits, and $e^{1.5} \approx 4.48$ is the perplexity. Nats use the natural logarithm, bits use base 2, and perplexity undoes the logarithm. The vocabulary size plays no role in the conversion.
:::
::::

Now the interpretation. A loss of $1.5$ nats means the model gives, on average in the geometric sense, probability $e^{-1.5} \approx 0.22$ to the character that actually comes next. A perplexity of $4.48$ means the model is, on average, as uncertain as if it were choosing uniformly among about four and a half characters, although English text uses more than 60 distinct characters.

::::predict{id=p2 kind=numeric answer=4.25 tol=0.15}
A model that knows nothing assigns every one of 70 possible characters probability $1/70$. What is its loss in nats per character? (A good character-level model on English reaches about 1.2 to 1.5.)

:::reveal
$-\ln(1/70) = \ln 70 \approx 4.25$ nats. The distance from $4.25$ down to about $1.3$ is everything the model has learned about spelling, words and grammar. Information theory gives you a floor too: no model can beat the entropy of the text itself.
:::
::::

## Why logarithms of probabilities?

Three properties single out $-\log p$ as the right measure of surprise:

- a certain event ($p = 1$) carries no surprise;
- rarer events are more surprising;
- the surprise of two independent events adds up, because probabilities multiply and logarithms turn products into sums.

The widget shows two distributions over four outcomes: $p$ (how the world behaves) and $q$ (what a model predicts). Drag the bars and watch the quantities named in the caption. Try making $q$ uniform, then making $q$ match $p$.

:::widget{name=EntropyBars k=4 p="4,3,2,1" q="1,1,1,1"}
:::

## Questions to carry into the derivation

1. Why is the average surprise of a model's predictions always at least the entropy of the data?
2. How does the gap between them, the KL divergence, behave, and why is it not symmetric?
3. Why does maximum likelihood training minimize exactly this quantity?
4. How short can a code for the text be, and how close does a practical code get?
