# Capstone: a policy-gradient agent with a measured baseline

Train a tabular softmax policy on a $5 \times 5$ gridworld with REINFORCE and a learned state-value baseline until its exact value is within 0.5 of the optimum that value iteration computes. Then measure what the baseline did: the variance of single-episode gradient estimates with and without it, at the trained policy, and check that it changed nothing on average.

:::exercise{ref=capstone}
:::

## When you finish

You can estimate gradients of expectations three ways and say which to use, evaluate and optimize policies in a Markov decision process, and explain what keeps policy-gradient training stable. L17 uses these estimators to train language models on rewards; M38 meets them again at the frontier.

:::edge{to=L17 text="policy gradients, baselines and KL regularization in RLHF."}
:::

:::edge{to=M38 text="training on rewards at scale."}
:::
