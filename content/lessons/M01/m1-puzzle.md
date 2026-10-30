# Puzzle: how much arithmetic is one forward pass?

A language model with one billion parameters reads a prompt of 1,000 tokens (a token is a word or a piece of a word). Before you know anything about how the model works inside, how many arithmetic operations does it perform?

No calculator, no formulas yet. Commit to an order of magnitude.

::::predict{id=p1 kind=choice answer=c}
Roughly how many floating-point operations (FLOPs: one multiplication or one addition of two decimal numbers) does the model perform to process one token?

- About a million, $10^6$.
- About a thousand million divided by a thousand, so $10^6$ again.
- About two billion, $2 \times 10^9$.
- About a trillion, $10^{12}$.

:::reveal
About $2 \times 10^9$. A parameter is a number the model multiplies something by. Processing one token uses each parameter once: multiply it by an input, then add the product to a running total. That is two operations per parameter, so about $2 \times 10^9$ per token for a billion parameters. You will build this count properly in the derivation.
:::
::::

## Build the answer from pieces

The prediction was a guess. Here is how to turn it into an estimate you can defend, without knowing the architecture.

A model's parameters live in tables of numbers called weight matrices. Feeding an input through one weight matrix with 1,000 rows and 1,000 columns means: for each of the 1,000 outputs, multiply each of the 1,000 inputs by its weight and add the products. That is $1{,}000 \times 1{,}000 = 10^6$ multiply-adds for $10^6$ parameters. One multiply-add per parameter, two FLOPs.

So the count does not depend on how the parameters are arranged: two FLOPs per parameter per token, whatever the shapes. For a 1,000-token prompt multiply again by 1,000.

::::predict{id=p2 kind=numeric answer=20 tol=8}
A laptop sustains about $10^{11}$ FLOPs per second on this kind of work. Using $2 \times 10^9$ FLOPs per token, how many seconds does the 1,000-token prompt take? Give a number of seconds.

:::reveal
$2 \times 10^9 \times 10^3 = 2 \times 10^{12}$ FLOPs, divided by $10^{11}$ FLOPs per second, is 20 seconds. A data-centre GPU sustains around $10^{14}$ to $10^{15}$, so it does the same work in a few hundredths of a second; that thousand-fold gap is why models are served from GPUs.
:::
::::

Estimates like this are products of a few factors, each only roughly known. The ladder below shows the estimate as a product of uncertain factors. Each factor has a low and a high guess; move them and watch two error bars: the worst case, where every factor errs in the same direction, and the typical case.

:::widget{name=MagnitudeLadder preset=forward}
:::

Notice that the typical error bar is much shorter than the worst case. Why should combining several uncertain numbers be more forgiving than the worst case suggests? That is the central question of this lesson.

## Questions to carry into the derivation

1. Why do we write $2 \times 10^{12}$ instead of 2,000,000,000,000, and what are the rules for multiplying numbers written that way?
2. How do units (seconds, bytes, FLOPs per second) combine, and how can they catch mistakes?
3. Why does a product of ten rough guesses usually land within a factor of ten of the truth?
4. Exactly how many FLOPs does a model spend per token, forward and in training?
