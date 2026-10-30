# Derivation: fine-tuning, LoRA and distillation

## 1. Supervised fine-tuning

An instruction example is a prompt $x$ and a response $y$. Fine-tuning maximizes the likelihood of the response given the prompt,
$$
\mathcal{L}_\text{SFT} = -\sum_{t \in \text{response}} \log p_\theta(y_t \mid x, y_{<t}),
$$
which is the language-modeling loss of L14 with a **mask** that keeps only the response positions. The prompt and response are joined by a **template** with special tokens (a separator, an end token), and the end token is part of the response, so the model learns to stop. Short examples are **packed** into long sequences with an attention mask that keeps them apart (exercise 9).

::::derivation{id=d1 title="Where the gradient goes"}
:::step
With a 30-token prompt and a 10-token response, an unmasked loss spends a fraction [[0.25|tol=0.001]] of its terms on the response.
:::
::::

## 2. Forgetting

Fine-tuning minimizes the new objective alone, and the gradient knows nothing about what pretraining taught. The weights drift, and the loss on the original distribution rises: **catastrophic forgetting**. Measure it directly, on the base evaluation, before and after. The remedies limit the drift: a small learning rate and few steps; **replay**, mixing some pretraining data into the fine-tuning batches; a penalty $\frac{\lambda}{2}\|\theta - \theta_\text{pre}\|^2$ that pulls the weights back (exercise 8); and training far fewer parameters.

## 3. LoRA: a low-rank update

LoRA (Hu et al., 2021) freezes each adapted weight $W_0$ and learns its change as a product of two thin matrices:
$$
W = W_0 + \frac{\alpha}{r} B A, \qquad A \in \mathbb{R}^{r \times d_\text{in}},\; B \in \mathbb{R}^{d_\text{out} \times r}.
$$
$B$ starts at zero, so training starts exactly at the pretrained model; $A$ starts random. The trainable parameters drop from $d_\text{in} d_\text{out}$ to $r (d_\text{in} + d_\text{out})$, the optimizer states with them, and after training $BA$ can be merged into $W_0$, so inference costs nothing extra. The scale $\alpha / r$ keeps the update's size comparable as $r$ changes.

Why should a low-rank update suffice? By Eckart-Young (M14), the best rank-$r$ approximation of any update is its truncated SVD, with error set by the discarded singular values. Measured fine-tuning updates of large models have rapidly decaying spectra (Aghajanyan et al., 2020, found that fine-tuning works in a small "intrinsic dimension"), so a small $r$ captures most of them. LoRA can represent any update of rank $r$ and nothing beyond: if the task needs more directions, the loss plateaus (exercise 12).

::::derivation{id=d2 title="Counting an adapter"}
:::step
A rank-8 adapter on a $4096 \times 4096$ matrix trains $8 \cdot (4096 + 4096) =$ [[65536]] parameters.
:::
:::step
That is a fraction $65536 / 4096^2 \approx$ [[0.0039|tol=0.0001]] of the matrix.
:::
::::

:::edge{from=M14 text="the SVD and the best low-rank approximation"}
:::

:::edge{from=L13 text="the weight matrices of a transformer block"}
:::

## 4. Distillation

A large **teacher** can train a small **student** with more than the right answers: its whole distribution over the next token says which wrong answers are nearly right. Hinton et al. (2015) soften both distributions with a temperature $T$ and minimize
$$
\mathcal{L} = \alpha\, T^2\, \mathrm{KL}\bigl(\operatorname{softmax}(t/T) \,\|\, \operatorname{softmax}(s/T)\bigr) + (1 - \alpha)\, \mathrm{CE}(s, y).
$$
The gradient of the KL term with respect to the student's logits is $(p_s - p_t)/T$, so the factor $T^2$ keeps its size independent of $T$. Raising $T$ flattens the distributions without changing their order, exposing the small probabilities. **Sequence-level distillation** (Kim and Rush, 2016) trains the student on the teacher's generated outputs instead, which needs no access to the teacher's probabilities.

::::derivation{id=d3 title="Softening"}
:::step
For logits $(2, 1, 0)$ at $T = 1$, the largest probability is about [[0.665|tol=0.002]].
:::
:::step
At $T = 2$ it falls to about [[0.506|tol=0.002]], and the smallest rises from 0.090 to about [[0.186|tol=0.002]].
:::
::::

:::edge{from=L19 text="the pretrained model"}
:::

## 5. Evaluating a fine-tune

Report two numbers: the **task metric** on held-out examples the model never trained on (here, exact-match accuracy on unseen inputs), and the **base evaluation**, the pretrained model's own loss, before and after, to measure forgetting. A fine-tune that wins the first and loses the second has traded one model for another.

:::edge{to=L21 text="Reinforcement learning starts from the fine-tuned model."}
:::

:::edge{to=L22 text="A distilled student is a natural draft model for speculative decoding."}
:::

:::edge{to=L24 text="The final capstone fine-tunes its own pretrained model."}
:::
