# Derivation: why runs break, and how to recover

## 1. The anatomy of a run

A training run is a loop around five things: a **configuration** fixed at the start, a **data stream** read from a position, the **model and optimizer**, a **schedule** that maps the step to a learning rate, and **checkpoints** that let it stop and restart. Around the loop sit **logging** (every step: loss, gradient norm before clipping, learning rate, throughput; every few hundred steps: validation loss), and an **evaluation harness**. Everything this lesson does is about making those parts trustworthy.

## 2. Where loss spikes come from

**The learning rate.** On a quadratic with curvature $\lambda$, gradient descent is stable only for $\eta < 2/\lambda$ (L05). Neural networks sharpen during training: the largest curvature rises until it reaches about $2/\eta$, where training hovers at the "edge of stability" (Cohen et al., 2021). Warmup lets the network reach flatter regions before the full rate; a rate that is too high, or a schedule bug, pushes it over the edge.

**The data.** A batch unlike the rest (binary junk, a corrupted shard, a document repeated thousands of times) produces a large gradient, and the update moves the model toward predicting junk.

**Adam's memory.** Adam divides by $\sqrt{\hat v}$, a running average of squared gradients. If a parameter's gradients have been near zero, $v$ decays toward zero, and a sudden gradient $g$ then gives $m = (1 - \beta_1) g$ and $v = (1 - \beta_2) g^2$: an update of size $(1 - \beta_1)/\sqrt{1 - \beta_2}$ times the learning rate, against about 1 in steady state.

::::derivation{id=d1 title="Adam after a quiet period"}
:::step
With $\beta_1 = 0.9$ and $\beta_2 = 0.999$, the first update after a long quiet period is $0.1/\sqrt{0.001} \approx$ [[3.162|tol=0.002]] times the learning rate.
:::
:::step
With $\beta_2 = 0.95$, the shorter memory gives [[0.447|tol=0.002]]: one reason large runs use $\beta_2 = 0.95$.
:::
::::

:::edge{from=L05 text="learning rates, warmup and stability"}
:::

**Numerics.** The softmax is unchanged when a constant is added to every logit, so output logits can drift to large values with nothing to stop them, until 16-bit arithmetic overflows (L13). Attention logits $q \cdot k/\sqrt{d}$ can grow too: the softmax collapses onto one position, its gradient vanishes, and training stalls or diverges (Dehghani et al., 2023; Wortsman et al., 2023).

## 3. Defenses in the model and the optimizer

**Gradient clipping.** Rescale all gradients by $\min(1, c/\|g\|)$, so no step moves the model more than a step with norm $c$ would. The gradient norm before clipping is the most sensitive alarm in the log: it usually jumps before the loss does.

**The z-loss.** PaLM added $10^{-4} (\log Z)^2$ to the loss, with $\log Z = \operatorname{logsumexp}(z)$. Its gradient with respect to the logits is $2 \cdot 10^{-4} \log Z \cdot p$, which pulls $\log Z$ toward zero without changing the predicted distribution's shape.

**QK-layernorm.** Normalize each head's queries and keys with a layer norm before their product. A normalized vector of dimension $d_h$ has norm $\sqrt{d_h}$, so by Cauchy-Schwarz
$$
\frac{|q \cdot k|}{\sqrt{d_h}} \le \frac{\sqrt{d_h}\,\sqrt{d_h}}{\sqrt{d_h}} = \sqrt{d_h},
$$
up to the learned gains.

::::derivation{id=d2 title="Bounded logits"}
:::step
With heads of dimension 64, the logits of normalized queries and keys are at most $\sqrt{64} =$ [[8]] (before gains).
:::
::::

## 4. Checkpoints and exact resume

A checkpoint is everything the next step depends on:

- the model's parameters and buffers;
- the optimizer state: Adam's $m$, $v$ **and step count** (the bias correction uses it);
- the gradient scaler of mixed precision (L13);
- the step, from which the learning rate is computed, and the **data position**;
- the random-number states that dropout and any shuffling draw from;
- the configuration, and the metrics log so far.

Write it to a temporary file and rename it into place, so a crash while saving never leaves a corrupt checkpoint. Test exact resume directly: $n$ steps straight must give the same weights as $k$ steps, save, load into a fresh process, and $n - k$ more.

**How often?** If writing a checkpoint takes $C$ seconds and failures arrive on average every $M$ seconds, checkpointing every $T$ seconds costs a fraction $C/T$ of the time in writing and loses on average $T/2$ per failure, a fraction $T/(2M)$. Minimizing $C/T + T/2M$ gives the Young/Daly interval
$$
T^* = \sqrt{2 C M}.
$$

::::derivation{id=d3 title="The checkpoint interval"}
:::step
With $C = 60$ s and one failure a day ($M = 86400$ s), $T^* = \sqrt{2 \cdot 60 \cdot 86400} \approx$ [[3220|tol=2]] seconds, about 54 minutes.
:::
:::step
The total overhead $C/T^* + T^*/2M$ is then about [[0.0373|tol=0.0005]] of the run.
:::
::::

:::edge{from=L12 text="a data pipeline that resumes exactly"}
:::

## 5. Detecting and recovering from spikes

Compare each step's loss, before trusting its update, with the mean and standard deviation of a trailing window, and flag it when it exceeds the mean by $k$ standard deviations; watch the gradient norm the same way. When a spike is flagged, the robust recovery is the one used to train PaLM: restart from a checkpoint before the spike and skip the data batches around it, which removes the bad data whether or not you know which batch it was. If spikes recur at the same place without bad data, lower the learning rate or add one of the defenses above.

The loss at step $s$ is computed before update $s$, so update $s - 1$ may already be damaged: restore the last checkpoint saved before it. Generating each batch from its data position makes skipping trivial: move the position.

## 6. Evaluation you can trust

The validation loss is a mean over examples, so report it with an interval: bootstrap the per-window losses (M25). Compare two checkpoints on the **same** windows with a paired difference, which is far more precise than comparing their separate intervals. Evaluate on fixed windows with fixed seeds, in evaluation mode, at regular steps, and never on training data.

:::edge{from=L11 text="the scaling fit that sized the run"}
:::

:::edge{from=L14 text="memory and data parallelism for the run"}
:::

## 7. The run report

A run is finished when its report is written: the configuration, the hardware and throughput, the loss curves, every incident (what was flagged, what was rolled back, what was skipped), the final evaluation with intervals, and what to change next time. The report is how the next run avoids the same failures.

:::edge{to=L16 text="Fine-tune the model you pretrained."}
:::

:::edge{to=L20 text="The final capstone runs this script end to end."}
:::
