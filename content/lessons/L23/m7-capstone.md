# Capstone: find a circuit and prove it

The notebook trains a two-layer, attention-only transformer on sequences of random tokens in which one block repeats. It learns to continue the second copy, and the question is how. You compute each head's previous-token and induction scores from its attention pattern and pick the candidate circuit; mean-ablate them and compare with ablating every other head; patch their clean outputs into a corrupted run, in which the first copy is replaced, and measure how much of the behaviour they restore; and test a prediction the mechanism makes about inputs the model never saw, a single earlier pair instead of a block, with a bootstrap interval. The notebook runs on a T4 in a few minutes, and on a CPU runtime in a little longer.

The autograder checks the score function on a hand-made attention pattern, that the model learned the task, that the circuit has a previous-token head in layer 0 and an induction head in layer 1, that ablating its previous-token heads, or its induction heads, sends the loss on the second copy close to uniform guessing while ablating every other head does less than half as much damage, that patching it restores most of the behaviour, that the prediction holds well above the control, and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L23}
:::

## When you finish

You have measured a model honestly and found a mechanism inside one. L24 brings every stage together: data, pretraining, fine-tuning, RL, evaluation and serving.

:::edge{to=L24 text="Evaluating every stage of the final pipeline."}
:::
