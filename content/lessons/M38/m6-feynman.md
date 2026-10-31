# Explain it plainly: a paper in five minutes

Teach the central idea of the paper you chose in five minutes to a learner who has finished M15, derivatives, but nothing after it.

Guidelines:

- Write 200 to 400 words.
- Use one small concrete example.
- Use only derivatives and arithmetic; explain any other idea you need in a sentence.
- Say what the idea assumes and when it would fail.

:::feynman{id=f1 prompt="Teach the central idea of the paper you chose (DPO, LoRA or Adam) in five minutes to a learner who has finished M15 but nothing after it." key_points="States the problem the paper solves in one or two plain sentences|States the central idea in one sentence before any detail|Works through one small concrete example with numbers|Uses only derivatives and arithmetic, explaining any other concept in a sentence when it first appears|Names the assumption the idea depends on and what happens when it fails"}
:::

## A written proof

:::feynman{id=proof1 prompt="Derive the DPO loss from the KL-regularized objective max over pi of E_pi[r] - beta KL(pi || pi_ref) and the Bradley-Terry model of preferences." key_points="States the Gibbs optimum pi* = pi_ref exp(r / beta) / Z of the KL-regularized objective|Inverts it to r = beta log(pi* / pi_ref) + beta log Z|Writes the Bradley-Terry likelihood of a preferred pair as sigma(r_w - r_l)|Substitutes the implied reward and shows that beta log Z cancels in the difference|Concludes that the negative log-likelihood is the DPO loss, a function of the policy and the reference only"}
:::
