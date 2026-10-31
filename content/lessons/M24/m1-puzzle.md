# Puzzle: averages of dice

Roll a fair die 30 times and record the average. Repeat many times, and draw a histogram of the averages.

::::predict{id=p1 kind=numeric answer=0.31 tol=0.05}
A single roll has standard deviation $\sqrt{35/12} \approx 1.71$. What is the standard deviation of the average of 30 rolls?

:::reveal
About $0.31$: $1.71/\sqrt{30}$. Thirty rolls make the average about five and a half times more precise than one roll, not thirty times.
:::
::::

::::predict{id=p2 kind=choice answer=b}
A single roll is flat: each face equally likely. What shape is the histogram of the averages?

- Flat between 1 and 6, like a single roll.
- A bell curve centered at 3.5.
- Flat between 3 and 4.
- Two peaks, near 1 and near 6.

:::reveal
A bell curve. Extreme averages need every roll to be extreme in the same direction, while middling averages can be reached in vastly more ways. The central limit theorem says more: whatever the distribution of one roll, as long as its variance is finite, the average is approximately Gaussian with mean $\mu$ and standard deviation $\sigma/\sqrt n$.
:::
::::

Start at one roll per average and slide $n$ upward. The histogram of standardized averages turns from flat to bell-shaped within a handful of rolls; try the skewed and coin distributions, which take longer, and the Cauchy, which never does.

:::widget{name=CLTMachine dist=die n=1}
:::

## Questions to carry into the derivation

1. How can you bound the chance of a large deviation knowing only a mean or a variance?
2. In what sense does an average converge to the mean?
3. Why a bell curve, and what does it require?
4. How do you compute an integral, or a probability of one in a million, by sampling, and how sure can you be of the answer?
