# Break it: leakage and tuning on the test set

Both failures in this movement produce impressive numbers from data that contain no signal at all.

## Feature selection outside the loop

You have 50 examples, 1,000 features of pure noise, and random labels. You pick the 20 features most correlated with the labels, then run 5-fold cross-validation of a simple classifier on those 20 features.

::::predict{id=p4 kind=choice answer=c}
What cross-validated accuracy do you expect?

- About 50 percent, since the data are noise.
- Below 50 percent, since noise features hurt.
- Well above 50 percent, often 75 to 90 percent.
- Exactly 100 percent.

:::reveal
The selection step saw every label, including the ones in each validation fold. Among 1,000 noise features, the 20 most correlated with these particular 50 labels are strongly correlated with them by chance, and cross-validation then rediscovers that chance correlation. Moving the selection inside each training fold brings the score back to about 50 percent.
:::
::::

:::exercise{ref=e10}
:::

## Choosing by test score

:::exercise{ref=e11}
:::

## What to take away

- Treat every label-dependent step as part of training. Put it inside the cross-validation loop or fit it on the training split only.
- Keep a final test set that you look at once. If you look at it twice to make a decision, you need a new one.
- The same mistakes happen at scale: a benchmark whose questions leaked into a pretraining corpus, or a team that picks checkpoints by benchmark score, reports numbers that will not hold up. L12 and L19 return to both.

:::edge{to=L12 text="Contamination of training data with evaluation data is this lesson's leak at the scale of the internet."}
:::
