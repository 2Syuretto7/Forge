# Capstone: RL with a verifiable reward, and what the KL penalty buys

The notebook fine-tunes a small GPT to add two-digit numbers from demonstrations in which 30% of the answers contain a slip (off by 1 or 10), as careless human data does. Maximum likelihood imitates the data: the supervised model gets most sums right when it decodes greedily, and slips about as often as its teachers when it samples. You then run RL against an exact verifier: write the reward, group-relative advantages and the policy-gradient loss with a KL penalty to the supervised model, and train two policies, one with a weak penalty (0.01) and one with a strong one (1.0). Both are compared with the supervised model on 500 held-out questions, item by item, for sampled and greedy accuracy, together with how far each moved from the supervised model in KL.

The autograder checks the reward, the advantages and the loss on small cases; that RL with the weak penalty raises held-out sampled accuracy with a paired interval whose lower end is above 0.1; that the strong penalty gives a policy closer to the supervised model and less accurate; and the report.

:::exercise{ref=capstone}
:::

:::colab{notebook=L21}
:::

## When you finish

The verifier here was better than the reference, so the penalty only held the policy back. With a learned reward model the roles reverse: the reward is wrong where the data was thin, and the penalty keeps the policy where the reward can be trusted. L23 asks how to evaluate a trained model honestly and how to look inside it.

:::edge{to=L23 text="Evaluating and interpreting the trained model."}
:::
