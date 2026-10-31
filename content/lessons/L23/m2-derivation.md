# Derivation: measuring a model and reading its activations

## 1. An evaluation is an estimate

A benchmark is a sample of items from the space of tasks it stands for, and an accuracy is an average over that sample. With per-item scores $c_i \in \{0, 1\}$ and accuracy $\hat p$, the standard error is $\sqrt{\hat p(1 - \hat p)/n}$; for scores that are not 0/1 (partial credit, log-probabilities), the percentile bootstrap of M25 gives an interval by resampling items. Items, not tokens or random seeds, are the unit to resample: they are what the benchmark sampled.

Comparing two models on the same items, the per-item difference $c^A_i - c^B_i$ has variance
$$
\operatorname{Var}(c^A - c^B) = \operatorname{Var}(c^A) + \operatorname{Var}(c^B) - 2 \operatorname{Cov}(c^A, c^B),
$$
and models find the same items hard, so the covariance is positive and a **paired** comparison is sharper than two separate intervals.

::::derivation{id=d1 title="The gain from pairing"}
:::step
Both models score 70%, so each per-item variance is $0.7 \cdot 0.3 = 0.21$. If the correlation between their item scores is 0.6, the paired variance per item is $0.42 - 2 \cdot 0.6 \cdot 0.21 =$ [[0.168|tol=0.001]].
:::
:::step
That is 0.4 of the unpaired variance, so the interval on the difference is narrower by a factor of $\sqrt{0.4} \approx$ [[0.63|tol=0.01]].
:::
:::step
For a 95% interval of $\pm 2$ points around an accuracy near 50%, $n = 1.96^2 \cdot 0.25 / 0.02^2 \approx$ [[2401|tol=1]] items are needed.
:::
::::

:::edge{from=M25 text="the bootstrap"}
:::

Sampling noise is only the first threat. **Contamination**: test items that appeared in the training data (L16) inflate scores exactly where they leaked; check with n-gram overlap and by comparing scores on items published before and after the training cutoff. **Prompt sensitivity**: formatting, few-shot examples and answer extraction can move scores by several points, so fix them and report them. **Seeds**: training randomness adds variance between checkpoints that the item interval does not cover; train several seeds when the claim is about a method. And a model trained against a reward (L21) can learn the grader's quirks, so evaluate with a held-out grader where possible.

:::edge{from=L21 text="a model shaped by rewards"}
:::

## 2. Linear probes

Does a model's hidden state $a \in \mathbb{R}^d$ encode a property $y$, such as the part of speech of the current token or whether a statement is true? A **linear probe** fits logistic regression $\sigma(w^\top a + b)$ on activations from one set of inputs and is scored on others. High held-out accuracy shows the property is **linearly decodable** from the activations; it does not show the model uses it, or that the probe found the model's own representation rather than something correlated with it.

Two controls separate what the representation contains from what the probe can learn. A probe on **random features** of the same dimension, or on an untrained model's activations, sets the baseline; a **control task** (Hewitt and Liang, 2019) assigns each word type a random but consistent label, and **selectivity** is the probe's accuracy on the real task minus that on the control. A probe flexible enough to learn the control task tells you about the probe, not the model. Keep probes linear and regularized, and confirm claims about use with interventions (section 5).

## 3. Superposition

A model with $d$ dimensions could give each feature its own orthogonal direction, which allows only $d$ features. Real models seem to represent far more by giving features directions that are only nearly orthogonal (Elhage et al., 2022). For random unit vectors, $\mathbb{E}[\cos^2] = 1/d$, and the number of directions with all pairwise overlaps below a fixed $\varepsilon$ grows exponentially with $d$.

The cost is **interference**: reading feature $i$ with its direction $v_i$ picks up $\sum_{j \ne i} (v_i^\top v_j) x_j$ from the other active features. If features are **sparse**, each active with small probability, few are active at once and the interference is small; the toy models of Elhage et al. show a phase change from one-feature-per-dimension to superposition as sparsity grows. A consequence is that individual neurons are often **polysemantic**, responding to several unrelated features, so the natural unit of analysis is a direction, not a neuron.

::::derivation{id=d2 title="Overlap in a residual stream"}
:::step
In a residual stream of 512 dimensions, two random directions have a typical cosine of $\sqrt{1/512} \approx$ [[0.044|tol=0.001]].
:::
::::

## 4. Sparse autoencoders

If activations are sparse combinations of many feature directions, we can try to recover the directions. A **sparse autoencoder** (SAE) with $m > d$ latents encodes and decodes
$$
z = \operatorname{ReLU}\bigl((x - b_d) W_e^\top + b_e\bigr), \qquad \hat x = z W_d + b_d,
$$
and minimizes $\|x - \hat x\|^2 + \lambda \|z\|_1$ averaged over activations. The reconstruction term asks the latents to explain $x$; the L1 term asks that few be active at once. The decoder rows are kept at unit norm, since otherwise the penalty could be avoided by shrinking $z$ and growing $W_d$. Each decoder row is a candidate feature direction, interpreted by the inputs that activate its latent most strongly (Bricken et al., 2023; Cunningham et al., 2023; Templeton et al., 2024).

Three numbers describe an SAE: the reconstruction error, the average number of active latents $L_0$, and the fraction of the model's loss recovered when its activations are replaced by the reconstruction. They trade off through $\lambda$: too little sparsity gives dense latents that mix features; too much loses information. Latents that never activate (**dead latents**) are common, and training resamples them toward badly reconstructed inputs. An SAE's features are a hypothesis about the model; whether the model uses them is tested by intervening on them.

## 5. Activation patching and circuits

Correlation is not mechanism: to show that a component carries the information behind a behaviour, change it and watch the output. **Activation patching** runs the model on a **clean** input and a **corrupted** one that differs in the relevant detail, picks a metric $m$ (such as the logit difference between the right and wrong answers), and reruns the corrupted input with one component's activation replaced by its clean value. The restored fraction
$$
\frac{m(\text{patched}) - m(\text{corrupt})}{m(\text{clean}) - m(\text{corrupt})}
$$
measures how much of the behaviour flows through that component. Patching clean into corrupted asks whether the component is **sufficient** to restore the behaviour; patching corrupted into clean asks whether it is **necessary**. **Ablation** removes a component instead, by zeroing it or, better, replacing it with its mean or with its value on another input, since zero may be far outside the activations the model ever sees.

::::derivation{id=d3 title="Reading a patching result"}
:::step
The logit difference is 3.2 on the clean input and $-0.8$ on the corrupted one. Patching one head gives 2.0, a restored fraction of [[0.7|tol=0.001]].
:::
::::

Patching every component costs one forward pass each. **Attribution patching** uses the first-order expansion $m(a_\text{clean}) - m(a_\text{corrupt}) \approx (a_\text{clean} - a_\text{corrupt})^\top \nabla_a m(a_\text{corrupt})$ to estimate all effects from one backward pass, accurate when the activations differ little; use it to rank candidates, then patch the top ones exactly.

A **circuit** is a set of components and the paths between them that implements a behaviour. The best understood is the **induction head** (Olsson et al., 2022): on a sequence $\ldots [A][B] \ldots [A]$, it predicts $[B]$. It needs two heads in different layers. A **previous-token head** in layer 1 writes into each position the identity of the token before it; the induction head in layer 2 then uses a query for the current token $[A]$ against keys that carry "the previous token was $[A]$", attends to the position of $[B]$ and copies it. The second head's keys are built from the first head's output, a composition through the residual stream. Induction heads form abruptly during training, and they let a model continue any pattern it has seen earlier in its context.

:::widget{name=AttentionHeatmap pattern=previous d=16}
:::

:::edge{from=L13 text="attention heads"}
:::

## 6. Making a claim

An interpretability claim names a mechanism and passes tests: the components found restore most of the behaviour when patched in (**sufficiency**), the behaviour drops when they are ablated (**necessity**), random components of the same size do neither, and the claim predicts something new, such as behaviour on a hand-made input. Report the effect sizes against these baselines, and the inputs where the account fails.

:::edge{to=L24 text="The final capstone evaluates its own model with intervals."}
:::
