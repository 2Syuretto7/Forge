# Derivation: policy gradients, RLHF, DPO and verifiable rewards

## 1. A language model is a policy

Given a prompt $x$, the model samples a response $y$ token by token, $\pi_\theta(y \mid x) = \prod_t \pi_\theta(y_t \mid x, y_{<t})$, and receives one reward $r(x, y)$ for the whole response. The objective is the expected reward,
$$
J(\theta) = \mathbb{E}_{x}\, \mathbb{E}_{y \sim \pi_\theta(\cdot \mid x)} \bigl[r(x, y)\bigr],
$$
which cannot be differentiated through the sampling directly.

## 2. The policy gradient

Since $\nabla \pi = \pi \nabla \log \pi$,
$$
\nabla_\theta J = \mathbb{E}_{y \sim \pi_\theta}\bigl[r(x, y)\, \nabla_\theta \log \pi_\theta(y \mid x)\bigr] = \mathbb{E}\Bigl[r(x, y) \sum_t \nabla_\theta \log \pi_\theta(y_t \mid x, y_{<t})\Bigr]:
$$
sample responses, and push up the log-probability of each in proportion to its reward. This is REINFORCE. For a softmax over logits, $\nabla \log \pi(a) = \text{onehot}(a) - p$: the same $p - y$ as L03's cross-entropy gradient, with the sign flipped and weighted by the reward. Supervised learning is the special case where every sampled action is the correct one with reward 1.

:::edge{from=L03 text="the gradient p - y of softmax cross-entropy"}
:::

## 3. Baselines and advantages

Because $\mathbb{E}[\nabla \log \pi] = \sum_y \nabla \pi(y) = \nabla 1 = 0$, subtracting any baseline $b$ that does not depend on the sampled response leaves the gradient unbiased, $\mathbb{E}[(r - b) \nabla \log \pi] = \nabla J$, and a good baseline (the expected reward) shrinks its variance enormously. The weight $r - b$ is the **advantage**: how much better than expected this response was. PPO learns a value function as the baseline and smooths it over steps with generalized advantage estimation; **GRPO** samples a group of responses to the same prompt and uses the group's mean reward as the baseline, normalized by its standard deviation, with no value network at all.

::::derivation{id=d1 title="Group advantages"}
:::step
A group of four responses earns rewards $(1, 0, 0, 0)$. The mean is 0.25 and the standard deviation $\sqrt{0.1875} \approx 0.433$, so the correct response's advantage is $0.75/0.433 \approx$ [[1.732|tol=0.002]].
:::
:::step
Each wrong one gets [[-0.577|tol=0.002]].
:::
::::

## 4. PPO

Generating responses is expensive, so PPO takes several gradient steps on each batch. The batch was sampled from the old policy, so each response is reweighted by $\rho = \pi_\theta(y)/\pi_\text{old}(y)$, and the objective is clipped so that one batch cannot move the policy far:
$$
L^\text{CLIP} = \mathbb{E}\bigl[\min\bigl(\rho A,\; \operatorname{clip}(\rho, 1 - \epsilon, 1 + \epsilon)\, A\bigr)\bigr].
$$
For a good response ($A > 0$) the gain stops at $\rho = 1 + \epsilon$; for a bad one it stops at $1 - \epsilon$.

## 5. The KL-regularized objective

RLHF maximizes the reward while staying close to a reference policy $\pi_\text{ref}$, the fine-tuned model:
$$
\max_\pi\; \mathbb{E}_{y \sim \pi}[r(y)] - \beta\, \mathrm{KL}(\pi \,\|\, \pi_\text{ref}).
$$
Over distributions on a set of responses this has a closed-form maximum. Writing the objective as $-\beta\,\mathrm{KL}\bigl(\pi \,\|\, \pi_\text{ref} e^{r/\beta}/Z\bigr) + \beta \log Z$, it is largest when the KL term vanishes:
$$
\pi^*(y) = \frac{1}{Z}\, \pi_\text{ref}(y)\, e^{r(y)/\beta}, \qquad Z = \sum_y \pi_\text{ref}(y)\, e^{r(y)/\beta}.
$$
Small $\beta$ lets the policy chase the reward; large $\beta$ keeps it near the reference.

::::derivation{id=d2 title="The tilted policy"}
:::step
With a reference $(0.5, 0.5)$, rewards $(0, 1)$ and $\beta = 1$, the optimum puts $e/(1 + e) \approx$ [[0.731|tol=0.002]] on the second response.
:::
:::step
With $\beta = 0.5$ it puts $e^2/(1 + e^2) \approx$ [[0.881|tol=0.002]] there.
:::
::::

:::edge{from=M27 text="the KL divergence as a leash"}
:::

## 6. Reward models from preferences

People judge "A is better than B" more consistently than they assign scores. The **Bradley-Terry** model links preferences to a scalar reward: $P(A \succ B) = \sigma(r(A) - r(B))$. A reward model is a language model with a scalar head trained on preference pairs by minimizing $-\log \sigma(r(y_w) - r(y_l))$. The classic RLHF pipeline (InstructGPT, 2022) is: supervised fine-tuning, then a reward model from human comparisons, then PPO against it with a KL penalty.

::::derivation{id=d3 title="Bradley-Terry"}
:::step
If $r(A) - r(B) = 1$, the model predicts $A$ is preferred with probability $\sigma(1) \approx$ [[0.731|tol=0.002]].
:::
::::

## 7. DPO: preferences without a reward model

Invert the optimum of section 5: $r(y) = \beta \log \frac{\pi^*(y)}{\pi_\text{ref}(y)} + \beta \log Z$. In the Bradley-Terry probability only reward differences appear, so $Z$ cancels:
$$
P(y_w \succ y_l) = \sigma\Bigl(\beta \log \frac{\pi(y_w)}{\pi_\text{ref}(y_w)} - \beta \log \frac{\pi(y_l)}{\pi_\text{ref}(y_l)}\Bigr).
$$
Fitting this likelihood to preference data trains the policy directly, with no reward model, no sampling and no RL (Rafailov et al., 2023). Its optimum is the same KL-regularized policy: exercise 8 checks it numerically.

::::derivation{id=d4 title="One DPO term"}
:::step
With $\beta = 0.1$ and a log-ratio difference of 2 in favour of the preferred response, the loss is $-\log \sigma(0.2) \approx$ [[0.598|tol=0.002]].
:::
::::

## 8. Verifiable rewards

When correctness can be checked (a math answer, a program's tests), the reward needs no model and cannot be flattered: 1 if the final answer is right, 0 otherwise, often with a small reward for the required format. RL with such rewards, using group advantages, trained the reasoning of models like DeepSeek-R1. It needs a policy that is already sometimes right: a group where every answer is wrong has all-zero advantages and teaches nothing, which is why RL comes after supervised fine-tuning.

## 9. What goes wrong

**Reward hacking.** The policy finds what the reward rewards, not what was meant: length, flattery, an answer format that fools the checker. **Overoptimization.** True quality peaks and falls as KL grows; watch it with held-out human or gold evaluations. **Collapse.** Without the KL penalty the policy concentrates on a few responses, its entropy goes to zero and it stops exploring.

:::edge{to=L19 text="Evaluating what the trained model actually learned."}
:::

:::edge{to=L20 text="The final capstone aligns its own model."}
:::
