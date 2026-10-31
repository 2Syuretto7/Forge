# Capstone: a dual SVM and the KL-regularized optimum

Solve a soft-margin SVM through its dual by coordinate ascent until its KKT residual is below $10^{-4}$, and check every point's category against complementary slackness. Then derive, implement and verify the KL-regularized optimum $\pi_ie^{r_i/\beta}/Z$: no random distribution may beat it, and $\log(p_i/\pi_i)$ must rise with slope exactly $1/\beta$ in the reward.

:::exercise{ref=capstone}
:::

## When you finish

You can certify an optimum, bound how far a solver is from one, and recognize softmax as the answer to a constrained problem. L01's ridge penalty is a multiplier; L17's DPO is the KL-regularized optimum read backwards; M38 asks you to find these structures in research papers.

:::edge{to=L17 text="RLHF and DPO, built on the KL-regularized optimum."}
:::

:::edge{to=L01 text="ridge regression as a constrained least-squares problem."}
:::
