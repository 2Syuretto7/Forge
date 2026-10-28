# Scale it: DPO and verifiable rewards

## DPO

::::predict{id=p3 kind=choice answer=b}
DPO and RLHF with PPO are trained on the same preference data with the same $\beta$. In the limit of unlimited data and optimization, their policies:

- Differ, because DPO has no reward model.
- Are the same: both reach the KL-regularized optimum of the Bradley-Terry reward.
- Differ, because DPO cannot use a KL penalty.
- Are the same only if $\beta = 1$.

:::reveal
DPO is derived from the same objective: its loss is the Bradley-Terry likelihood written in terms of the policy that would be optimal for that reward. In practice they differ because data and optimization are finite, PPO samples new responses while DPO only sees the dataset, and the reward model generalizes differently from the implicit one.
:::
::::

:::exercise{ref=e08}
:::

## Rewards you can check

:::exercise{ref=e09}
:::

:::exercise{ref=e10}
:::
