# Recall bridge: KL, the score function and a fine-tuned model

From M27: the KL divergence measures how far one distribution is from another, and it is never negative. From L07: the gradient of softmax cross-entropy with respect to the logits is $p - y$. From L20: supervised fine-tuning teaches a model to imitate good responses. This lesson asks for more than imitation: improve the model on what we actually want, measured by a reward, without letting it drift into nonsense. Reviews due from M27, L07 and L20 appear above.

::::derivation{id=d0 title="Warm-up"}
:::step
For a softmax policy with probabilities $(0.7, 0.2, 0.1)$, the gradient of $\log p_3$ with respect to the third logit is $1 - 0.1 =$ [[0.9]].
:::
:::step
With respect to the first logit it is [[-0.7]].
:::
:::step
$\mathrm{KL}(p \,\|\, p) =$ [[0]] for any distribution $p$.
:::
::::
