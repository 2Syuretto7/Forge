# Break it: averaging gradients wrongly

Each rank holds the **sum** of its examples' gradients and how many examples it had (the last batch of an epoch is often smaller).

1. `correct_average(grad_sums, counts)`: the full-batch mean gradient.
2. `mean_of_means(grad_sums, counts)`: the common bug of averaging the ranks' means.
3. `sum_of_means(grad_sums, counts)`: the bug of all-reducing with a sum and not dividing by the number of ranks.

## Hints

1. The correct mean divides the total gradient by the total count.
2. The mean of means is right only when every rank has the same count; otherwise examples on small ranks weigh more.
3. Summing without dividing multiplies the gradient, and so the learning rate, by the number of ranks: a run that worked on 8 GPUs diverges on 64.
