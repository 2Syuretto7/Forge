# Derivation: loss, compute and the best allocation

## 1. Power laws, and why loss is predictable

Across many orders of magnitude, the validation loss of language models falls smoothly as models, data and compute grow, and it is well described by power laws with a floor:
$$
L(N) \approx E + A N^{-\alpha}, \qquad L(D) \approx E + B D^{-\beta}.
$$
$E$ is the loss that no model can remove, the entropy of the text itself (M27); $A N^{-\alpha}$ is the excess loss due to a finite model. A power law has no characteristic scale: multiplying $N$ by 10 multiplies the excess by $10^{-\alpha}$ whatever $N$ is, which is why a fit on small models says something about large ones.

Why power laws? One account: the loss is a sum of many contributions, like rare words, idioms or facts, each learned at its own rate. If a component with rate $t$ decays as $e^{-xt}$ in the resources $x$ and the rates are spread with density proportional to $t^{s-1}$, the total is
$$
\int_0^\infty t^{s-1} e^{-x t}\, dt = \Gamma(s)\, x^{-s},
$$
a power law, even though every component decays exponentially.

::::derivation{id=d1 title="Reading a power law"}
:::step
With $A = 406.4$ and $\alpha = 0.34$, the excess loss of a model with $N = 10^9$ parameters is $406.4 \cdot 10^{-3.06} \approx$ [[0.354|tol=0.001]] nats.
:::
:::step
Ten times more parameters multiply that excess by $10^{-0.34} \approx$ [[0.457|tol=0.001]].
:::
:::step
For $s = 0.5$ and $x = 4$, the integral is $\Gamma(0.5) \cdot 4^{-0.5} = \sqrt{\pi}/2 \approx$ [[0.886|tol=0.001]].
:::
::::

:::edge{from=L02 text="error against capacity and data"}
:::

## 2. Counting compute: C = 6ND

A linear layer $y = Wx$ with $W$ of shape $m \times n$ does $mn$ multiply-adds per token, $2mn$ FLOPs: **2 FLOPs per parameter in the forward pass**. The backward pass computes two products of the same size, $W^\top g$ for the input gradient and $g x^\top$ for the weight gradient: **4 more**. Since almost all parameters of a transformer sit in such matrices, training costs about $6N$ FLOPs per token and
$$
C \approx 6 N D.
$$
Attention adds work that does not appear in the parameter count: per layer and token, the scores against `ctx` keys and the weighted sum of values cost $4\,\text{ctx}\,d$ in forward, so $12\,n_\text{layer}\,\text{ctx}\,d$ in training. With $N \approx 12\,n_\text{layer} d^2$, attention's share of the FLOPs is $\text{ctx} / (6d + \text{ctx})$: small for wide models, large for narrow models with long contexts. Scaling-law studies count the **non-embedding** parameters, since embedding lookups cost almost nothing.

::::derivation{id=d2 title="Counting"}
:::step
GPT-3 has 175 billion parameters and was trained on 300 billion tokens: $C = 6ND \approx$ [[3.15e23|tol=2e21]] FLOPs.
:::
:::step
Its context of 2048 tokens and width $d = 12288$ give an attention share of $2048 / (6 \cdot 12288 + 2048) \approx$ [[0.027|tol=0.001]].
:::
:::step
The L10 capstone model ($d = 192$, context 128) spends a fraction [[0.1|tol=0.002]] of its FLOPs on attention.
:::
::::

:::edge{from=L10 text="the GPT whose loss we now scale"}
:::

## 3. The compute-optimal allocation

Model the loss as a function of both resources (Hoffmann et al., 2022):
$$
L(N, D) = E + \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}}.
$$
For a fixed budget, substitute $D = C/(6N)$ and minimize over $N$. Working in $\log N$ (so that raising $N$ by a factor lowers $D$ by the same factor):
$$
\frac{dL}{d \log N} = -\alpha A N^{-\alpha} + \beta B D^{-\beta} = 0
\quad\Longrightarrow\quad
\alpha A N^{-\alpha} = \beta B D^{-\beta}.
$$
Substituting $D = C/(6N)$ and solving for $N$:
$$
N^* = G \left(\frac{C}{6}\right)^{\frac{\beta}{\alpha + \beta}}, \qquad
D^* = G^{-1} \left(\frac{C}{6}\right)^{\frac{\alpha}{\alpha + \beta}}, \qquad
G = \left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha + \beta}}.
$$
On this frontier both excess terms scale as $(C/6)^{-\gamma}$ with $\gamma = \alpha\beta/(\alpha + \beta)$, so the best achievable loss is again a power law with a floor, $L^*(C) = E + K (C/6)^{-\gamma}$. The optimality condition also says how the excess splits: the parameter term is $\beta/\alpha$ times the data term.

::::derivation{id=d3 title="The exponents"}
:::step
With Hoffmann et al.'s fitted $\alpha = 0.34$ and $\beta = 0.28$, the optimal model size grows as $C^{a}$ with $a = \beta/(\alpha + \beta) \approx$ [[0.4516|tol=0.0005]].
:::
:::step
The frontier falls as $C^{-\gamma}$ with $\gamma = \alpha\beta/(\alpha + \beta) \approx$ [[0.1535|tol=0.0005]].
:::
:::step
So ten times the compute multiplies the best excess loss by $10^{-\gamma} \approx$ [[0.702|tol=0.002]]: a 30% cut, at ten times the cost.
:::
:::step
If $\alpha = \beta$, both $N^*$ and $D^*$ grow as $C$ to the power [[0.5]], and the ratio of tokens to parameters stays fixed.
:::
::::

## 4. What the experiments found

Kaplan et al. (2020) trained models up to about a billion parameters and fitted $N^* \propto C^{0.73}$: put most of a larger budget into a larger model. Hoffmann et al. (2022) trained over 400 models, from 70 million to 16 billion parameters, with three methods: the lower envelope of training curves, IsoFLOP profiles (exercise 7), and fitting the parametric law above (exercises 4 and 5). The first two gave $N^* \propto C^{0.5}$ and about **20 tokens per parameter**. They pointed out that the earlier study had used one learning-rate schedule length for runs of different token counts, which understates what shorter runs achieve when their schedule matches their length. The test was Chinchilla: 70 billion parameters on 1.4 trillion tokens, with the compute of the 280-billion-parameter Gopher trained on 300 billion tokens, and better on almost every benchmark.

The published constants of the third method imply a ratio that drifts upward with compute (the widget shows about 98 tokens per parameter at $10^{24}$ FLOPs). A later replication (Besiroglu et al., 2024) argued that this fit was imprecise and that a refit agrees with the other two methods. The lesson for your own fits: report uncertainties, and check a fitted law against the methods that do not depend on its functional form.

::::predict{id=p3 kind=numeric answer=5.88e23 tol=0.05e23}
Chinchilla has 70 billion parameters and saw 1.4 trillion tokens. Using $C = 6ND$, what was its training compute in FLOPs?

:::reveal
$6 \cdot 7 \times 10^{10} \cdot 1.4 \times 10^{12} = 5.88 \times 10^{23}$ FLOPs, close to Gopher's $6 \cdot 2.8 \times 10^{11} \cdot 3 \times 10^{11} = 5.04 \times 10^{23}$. Same compute, a quarter of the parameters, four to five times the tokens: 20 tokens per parameter instead of about 1.
:::
::::

## 5. Beyond compute-optimal: paying for inference

Compute-optimal means the lowest loss for a training budget. But a deployed model costs about $2N$ FLOPs for every token it serves, so if it will serve $D_\text{inf}$ tokens, the cost of reaching a target loss is $6ND + 2ND_\text{inf}$. Minimizing that favors a **smaller model trained on more tokens** than the Chinchilla rule: for example, LLaMA (2023) trained a 7-billion-parameter model on a trillion tokens, about 150 tokens per parameter. Exercise 9 finds the cheapest model for a target loss and an inference load.

## 6. Fitting scaling laws in practice

- **Fit in log space.** Losses span a range, and relative errors matter. Hoffmann et al. minimized the Huber loss of $\log \hat L - \log L$, with $\log \hat L$ written as a log-sum-exp of $a - \alpha \log N$, $b - \beta \log D$ and $e$ (exercise 4).
- **Use the structure.** With the exponents fixed, the law is linear in $(E, A, B)$; searching over the two exponents and solving a small least-squares problem for each is far more reliable than gradient descent on all five (exercise 5).
- **Predict, then check.** Hold out the largest run, fit on the rest, and compare. The individual constants are often poorly determined (half a percent of noise can move $B$ by 30%) while predictions inside and near the fitted range stay accurate.
- **Report uncertainty.** Bootstrap the runs and refit to get intervals on exponents and predictions (exercise 8).
- **Fit over a wide range, with a floor.** The frontier bends toward $E$; a pure power law fitted over a narrow range extrapolates optimistically (exercise 11).
- **Retune what changes with scale.** The best learning rate shrinks as models grow (L05); sweeping sizes at one rate makes large models look worse and flattens the fitted exponent (exercise 12).

:::edge{from=L05 text="learning rates must be retuned across sizes"}
:::

## 7. When data runs out, and when it is not all equal

The law assumes every token is fresh. Muennighoff et al. (2023) found that repeating data for up to about four epochs is nearly as good as new data, after which returns fall off; they model $U$ unique tokens seen for $1 + R$ epochs as worth $U + U R^*(1 - e^{-R/R^*})$ fresh ones (exercise 10). Data quality matters too: deduplicated, filtered data moves the whole curve down, which is L12's subject.

:::edge{from=L12 text="data quality shifts the scaling curve"}
:::

:::edge{to=L14 text="Large models need many GPUs: parallelism."}
:::

:::edge{to=L15 text="A real pretraining run, sized with these laws."}
:::

:::edge{to=L20 text="Your scaling fit sizes the capstone model and token budget."}
:::
