# Explain it plainly: training a model with rewards

Explain to an engineer how a language model is improved with reinforcement learning from a reward, and why the KL penalty is there.

- Write 150 to 400 words.
- Explain the policy gradient and the role of a baseline.
- Explain where rewards come from: preferences and a reward model, or an exact check.
- Explain the KL penalty and one way optimization against a reward goes wrong; mention DPO.

:::feynman{id=f1 prompt="Explain how reinforcement learning improves a language model using a reward, where the reward comes from, why a KL penalty to the starting model is used, and how DPO relates; include one way reward optimization goes wrong." key_points="The policy gradient raises the log-probability of sampled responses in proportion to their reward, estimated from samples|Subtracting a baseline such as the mean reward of a group of samples reduces variance without bias|Rewards come from a reward model trained on human preferences with the Bradley-Terry model, or from an exact check such as a correct math answer|The KL penalty keeps the policy near the starting model, where the reward model is trustworthy, and prevents collapse|Optimizing a flawed reward too hard raises the reward while true quality falls, which is reward hacking|DPO trains directly on preferences by writing the reward in terms of the policy's log-probability ratio to the reference"}
:::
