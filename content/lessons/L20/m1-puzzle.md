# Puzzle: how large a model for a small corpus?

Your corpus is Tiny Shakespeare, about 1 million training bytes, and your budget is one T4 for an afternoon.

::::predict{id=p1 kind=numeric answer=50000 tol=0.05}
The Chinchilla rule of thumb is about 20 training tokens per parameter. By that rule, how many parameters should a model trained on 1 million tokens have?

:::reveal
$10^6 / 20 = 50{,}000$ parameters. Yet the model of L15, with 10.7 million parameters trained for about 40 epochs with dropout, reaches a validation loss far below what a 50,000-parameter model can reach (Karpathy's nanoGPT reports about 1.47 nats per character for this configuration). The Chinchilla rule answers a different question: the best split of a fixed **compute** budget when data is unlimited. Here data is the limit and compute is plentiful, so the right move is a larger model that sees the same data many times, with regularization and early stopping on a validation set (Muennighoff et al., 2023, measure how repeated data loses value). Your design document has to make exactly this kind of argument.
:::
::::

The widget fits scaling curves to runs of different sizes. Use it to recall what the fitted law predicts, and what it assumes about data.

:::widget{name=ScalingFit}
:::

:::edge{from=L11 text="sizing a model from a budget"}
:::

::::predict{id=p2 kind=choice answer=c}
The pipeline pretrains, fine-tunes with LoRA, then runs RL against an exact-match reward. Which evaluation tells you whether RL helped?

- The RL reward at the end of training.
- Accuracy on the training prompts before and after RL.
- Accuracy with confidence intervals on held-out prompts, before and after RL, compared item by item, with the base model's loss on ordinary text to show what was lost.
- The KL divergence from the reference policy.

:::reveal
Training reward measures what was optimized, on the inputs it was optimized on; it can rise through memorization or reward hacking. A held-out, paired comparison with intervals (L19) tells you whether the change generalizes and whether it is larger than noise, and the base loss measures forgetting (L16). The KL is a diagnostic of how far the policy moved, not of whether it improved.
:::
::::
