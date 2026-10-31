# Derivation: surprise, codes and divergence

Information theory gives one number for "how surprised you are", then builds everything else from it: the average surprise of a source (entropy), the average surprise of a model about that source (cross-entropy), the gap between the two (KL divergence), and how much one variable tells you about another (mutual information). Along the way you will see why training a classifier or a language model by maximum likelihood is the same as minimizing cross-entropy, and how that loss turns into bits on a disk.

## 1. Surprisal and entropy

The **surprisal** of an outcome with probability $p$ is $-\log p$. In base 2 it is measured in **bits**, in base $e$ in **nats**; one nat is $1/\ln 2 \approx 1.44$ bits. The **entropy** of a distribution is its expected surprisal,

$$
H(p) = -\sum_x p(x) \log p(x),
$$

with the convention $0 \log 0 = 0$ (impossible outcomes contribute nothing). Entropy is the uncertainty of a source before you see its output.

::::derivation{id=d1 title="Entropies you should know by heart"}
:::step
A fair coin has entropy $-2 \cdot \tfrac12 \log_2 \tfrac12 =$ [[1]] bit.
:::
:::step
The distribution $(\tfrac12, \tfrac14, \tfrac14)$ has entropy $\tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac14 \cdot 2 =$ [[1.5]] bits.
:::
:::step
A uniform distribution over $K$ outcomes has entropy $\log K$. In nats, a uniform choice among 70 characters has entropy $\ln 70 \approx$ [[4.248]].
:::
:::step
A coin with $P(\text{heads}) = p$ has entropy $h(p) = -p\log p - (1-p)\log(1-p)$. Its derivative is $h'(p) = \log\dfrac{1-p}{p}$, which is zero at $p =$ [[0.5]], where the entropy is largest.
:::
::::

Entropy lies between $0$ (a certain outcome) and $\log K$ (uniform over $K$ outcomes). The upper bound follows from Gibbs' inequality below.

## 2. Entropy as the length of the best code

Suppose you must transmit outcomes of a source as binary strings, using a **prefix code** (no codeword is the start of another, so a stream decodes unambiguously). Codeword lengths $\ell(x)$ are achievable by a prefix code exactly when they satisfy the **Kraft inequality** $\sum_x 2^{-\ell(x)} \le 1$.

Shannon's **source coding theorem**: the expected length of any prefix code satisfies $\mathbb{E}[\ell] \ge H(p)$ bits, and choosing $\ell(x) = \lceil -\log_2 p(x) \rceil$ achieves $\mathbb{E}[\ell] < H(p) + 1$. Rare outcomes get long codewords, common ones short codewords, and the ideal length of a codeword is its surprisal. Huffman's algorithm, which you will implement in the capstone, finds the optimal prefix code.

::::derivation{id=d2 title="Shannon code lengths"}
:::step
For $p = (\tfrac12, \tfrac14, \tfrac18, \tfrac18)$ the Shannon lengths are $1, 2, 3, 3$. The Kraft sum is $\tfrac12 + \tfrac14 + \tfrac18 + \tfrac18 =$ [[1]].
:::
:::step
The expected length is $\tfrac12 \cdot 1 + \tfrac14 \cdot 2 + \tfrac18 \cdot 3 \cdot 2 =$ [[1.75]] bits, which equals the entropy exactly because every probability is a power of $\tfrac12$.
:::
::::

## 3. Cross-entropy and KL divergence

Now suppose the source follows $p$ but you designed your code for a model $q$, giving outcome $x$ a codeword of length $-\log q(x)$. The expected length is the **cross-entropy**

$$
H(p, q) = -\sum_x p(x) \log q(x).
$$

The excess over the best possible code is the **Kullback-Leibler divergence**

$$
\mathrm{KL}(p \,\|\, q) = H(p, q) - H(p) = \sum_x p(x) \log \frac{p(x)}{q(x)} .
$$

It is the expected number of extra bits (or nats) you pay for believing $q$ when the truth is $p$.

**Gibbs' inequality** says $\mathrm{KL}(p \,\|\, q) \ge 0$, with equality only when $q = p$. The proof needs only the fact that $\log x \le x - 1$ for $x > 0$, with equality only at $x = 1$.

::::derivation{id=d3 title="Gibbs' inequality"}
:::step
Write $-\mathrm{KL}(p\|q) = \sum_x p(x) \log \dfrac{q(x)}{p(x)}$, summing over outcomes with $p(x) > 0$. Applying $\log t \le t - 1$ with $t = q(x)/p(x)$ bounds each term by $p(x)\big(q(x)/p(x) - 1\big) =$ [[q - p]], writing p and q for $p(x)$ and $q(x)$.
:::
:::step
Summing, $-\mathrm{KL} \le \sum_x q(x) - \sum_x p(x) \le 1 - 1 =$ [[0]]. So $\mathrm{KL} \ge 0$.
:::
:::step
Equality requires $q(x)/p(x) = 1$ wherever $p(x) > 0$. Taking $q$ uniform over $K$ outcomes gives $\mathrm{KL}(p\|q) = \log K - H(p) \ge 0$, which proves the bound $H(p) \le$ [[log(K)]].
:::
::::

KL is **not symmetric**, and it is not a distance.

::::derivation{id=d4 title="The two KL divergences differ"}
:::step
Let $p = (0.5, 0.5)$ and $q = (0.9, 0.1)$. Then $\mathrm{KL}(p\|q) = 0.5 \ln\tfrac{0.5}{0.9} + 0.5 \ln\tfrac{0.5}{0.1} \approx$ [[0.5108]] nats.
:::
:::step
And $\mathrm{KL}(q\|p) = 0.9 \ln\tfrac{0.9}{0.5} + 0.1 \ln\tfrac{0.1}{0.5} \approx$ [[0.3681]] nats.
:::
:::step
If $q(x) = 0$ for some $x$ with $p(x) > 0$, then $\mathrm{KL}(p\|q)$ is infinite. A model that declares an observed event impossible pays an infinite penalty; you met this in M25 as the tiny-sample MLE.
:::
::::

The asymmetry has a sharp practical consequence when you fit a simple $q$ to a complicated $p$. Minimizing $\mathrm{KL}(p\|q)$ (the **forward** KL) punishes $q$ for missing any region where $p$ has mass, so $q$ spreads out to **cover** all of $p$. Minimizing $\mathrm{KL}(q\|p)$ (the **reverse** KL) punishes $q$ for putting mass where $p$ has little, so $q$ **locks onto one mode**. You will see both in Movement 5.

:::edge{to=L21 text="RLHF penalizes KL(policy || reference): a reverse KL that keeps the policy inside what the reference model considers plausible."}
:::

**Gaussians.** For two univariate Gaussians the KL has a closed form, derived by taking the expectation of $\log p - \log q$ under $p$:

$$
\mathrm{KL}\big(\mathcal N(\mu_1,\sigma_1^2) \,\|\, \mathcal N(\mu_2,\sigma_2^2)\big) = \log\frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2\sigma_2^2} - \frac12 .
$$

::::derivation{id=d5 title="Checking the Gaussian formula"}
:::step
With equal variances $\sigma_1 = \sigma_2 = \sigma$, the formula reduces to $\dfrac{(\mu_1 - \mu_2)^2}{2\sigma^2}$. For $\mu_1 - \mu_2 = 2$ and $\sigma = 1$ that is [[2]] nats.
:::
:::step
With equal means, $\mu_1 = \mu_2$, and $\sigma_2 = 2\sigma_1$, the KL is $\ln 2 + \tfrac{1}{8} - \tfrac12 \approx$ [[0.3181]] nats.
:::
::::

## 4. Maximum likelihood is minimum cross-entropy

Given data $x_1, \dots, x_n$, let $\hat p$ be the **empirical distribution** that puts mass $1/n$ on each observation. The average negative log-likelihood of a model $q$ is

$$
-\frac{1}{n}\sum_{i=1}^n \log q(x_i) = -\sum_x \hat p(x) \log q(x) = H(\hat p, q) = H(\hat p) + \mathrm{KL}(\hat p \,\|\, q).
$$

$H(\hat p)$ does not depend on the model. So maximizing likelihood, minimizing the cross-entropy loss, and minimizing the forward KL from the data to the model are the same optimization. Every classifier and language model in this course is trained this way, and its loss is reported in nats.

:::edge{from=M25 text="maximum likelihood estimation"}
:::

## 5. The gradient of softmax cross-entropy

For a classifier with logits $z$ and target class $y$, the loss is $\ell = -\log p_y$ with $p = \operatorname{softmax}(z)$. Compute it stably as $\ell = \operatorname{LSE}(z) - z_y$, where $\operatorname{LSE}(z) = m + \log\sum_k e^{z_k - m}$ with $m = \max_k z_k$, so no exponential ever overflows.

::::derivation{id=d6 title="The famous p minus onehot"}
:::step
The derivative of $-\log p_y$ with respect to $p_y$ is $-1/p_y$, so the upstream gradient is $u = -e_y / p_y$. By M19, the softmax VJP is $p \odot (u - u^\top p)$. Here $u^\top p = -p_y/p_y =$ [[-1]].
:::
:::step
So the gradient with respect to $z_j$ is $p_j\,(u_j + 1)$. For $j \neq y$, $u_j = 0$ and the gradient is $p_j$. For $j = y$, it is $p_y(-1/p_y + 1) =$ [[p - 1]], writing p for $p_y$.
:::
:::step
Together, $\nabla_z \ell = p - e_y$: predicted probabilities minus the one-hot target. With logits $(2, 0)$ and target class 2 (the second), the gradient on the second logit is $p_2 - 1 \approx$ [[-0.8808]].
:::
::::

Directly differentiating $\operatorname{LSE}(z) - z_y$ gives the same answer faster: $\partial\operatorname{LSE}/\partial z_j = p_j$. This gradient never involves a division by a small probability, which is why the fused "cross-entropy from logits" is both fast and stable.


## 6. Mutual information and conditional entropy

For a pair of variables with joint distribution $p(x, y)$, the **conditional entropy** $H(Y \mid X) = -\sum_{x,y} p(x,y)\log p(y \mid x)$ is the uncertainty left about $Y$ once $X$ is known. The **chain rule** $H(X, Y) = H(X) + H(Y \mid X)$ follows from $\log p(x,y) = \log p(x) + \log p(y\mid x)$.

The **mutual information** is how much knowing $X$ reduces uncertainty about $Y$:

$$
I(X; Y) = H(Y) - H(Y \mid X) = \mathrm{KL}\big(p(x, y) \,\|\, p(x)\,p(y)\big) \ge 0 .
$$

So **conditioning never increases entropy on average**: $H(Y \mid X) \le H(Y)$.

::::derivation{id=d7 title="Two extreme couplings"}
:::step
If $X$ and $Y$ are independent, $p(x,y) = p(x)p(y)$ and $I(X;Y) =$ [[0]].
:::
:::step
If $Y = X$ for a fair coin $X$, then $H(Y \mid X) = 0$ and $I(X;Y) = H(Y) =$ [[1]] bit.
:::
::::

This is why language modeling works at all. The entropy of the next character with no context is about 4 bits for English; given the previous character it drops; given the previous hundred characters it drops much further. A language model is a learned estimate of $p(\text{next token} \mid \text{context})$, and its loss approaches the conditional entropy of text given its context.

## 7. Units: nats, bits and perplexity

A per-token cross-entropy $L$ in nats converts to **bits per token** $L / \ln 2$ and to **perplexity** $e^{L}$, the size of a uniform choice with the same average surprise. All three are monotone in each other: lower is better for all of them, and they rank models identically.

:::edge{to=L14 text="Your GPT's validation loss, bits per character and perplexity are this section's three units."}
:::

:::edge{to=L06 text="Held-out cross-entropy is the generalization measure for probabilistic models."}
:::

## Summary

| Quantity | Formula | Meaning |
| --- | --- | --- |
| Surprisal | $-\log p(x)$ | bits or nats to encode $x$ |
| Entropy | $H(p) = -\sum p \log p$ | best average code length |
| Cross-entropy | $H(p,q) = -\sum p\log q$ | average loss of model $q$ on data from $p$ |
| KL | $\sum p \log(p/q) \ge 0$ | extra cost of $q$ over the truth |
| Mutual information | $H(Y) - H(Y\mid X)$ | what $X$ tells you about $Y$ |
| CE gradient | $\operatorname{softmax}(z) - e_y$ | every classifier's backward pass |
| Perplexity | $e^{L}$ | effective number of choices |
