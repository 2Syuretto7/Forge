# Derivation: tokens, likelihood and sampling

## 1. Language modeling is cross-entropy minimization

A language model assigns a probability to a sequence by the chain rule:
$$
p(x_1, \dots, x_n) = \prod_{t=1}^{n} p(x_t \mid x_{<t}).
$$
Training minimizes the average negative log-likelihood of the training tokens, $-\tfrac1n \sum_t \ln p(x_t \mid x_{<t})$: the cross-entropy between the data and the model (M27). The causal transformer (L13) computes all $n$ conditionals in one pass. The loss is reported in **nats per token**; $e^{\text{loss}}$ is the **perplexity**; and to compare tokenizers, convert to **bits per character**:
$$
\text{bits per character} = \frac{\text{nats per token}}{\text{characters per token} \cdot \ln 2}.
$$

::::derivation{id=d1 title="Units"}
:::step
A loss of 1.5 nats per token with 2 characters per token is $1.5/(2 \ln 2) \approx$ [[1.082|tol=0.002]] bits per character.
:::
:::step
Its perplexity per token is $e^{1.5} \approx$ [[4.48|tol=0.01]].
:::
::::

:::edge{from=M27 text="cross-entropy, bits and perplexity"}
:::

## 2. Byte-pair encoding

Start from the UTF-8 bytes of the training text, with a vocabulary of the 256 byte values. Repeatedly count every adjacent pair of tokens, pick the most frequent, give it a new id, and replace its occurrences (left to right, without overlaps). Each merge adds one token. To encode new text, take its bytes and apply the learned merges, earliest first. To decode, look up each id's byte string and decode the concatenation as UTF-8.

::::derivation{id=d2 title="One merge"}
:::step
In the string "aaabdaaabac", the pair "aa" occurs [[4]] times, counting overlaps.
:::
:::step
Replacing it left to right without overlaps by a new symbol Z gives "ZabdZabac", of length [[9]].
:::
:::step
A vocabulary of 50,257 tokens embedded in $d = 768$ dimensions takes $50257 \cdot 768 =$ [[38597376]] parameters.
:::
::::

**Pre-tokenization.** Counting pairs across the whole text lets merges cross word boundaries ("e t" from "the tree"), wasting vocabulary on accidents. GPT-2 first splits the text with a regular expression into chunks (words with their leading space, numbers, punctuation, whitespace) and merges only within chunks. Counting each distinct chunk once, weighted by its frequency, also makes training fast.

**The vocabulary-size trade-off.** A larger vocabulary means fewer tokens per text (a longer effective context, fewer steps per epoch) but a larger embedding and output layer, and rarer tokens whose embeddings see few updates.

## 3. From text to training windows

Encode the corpus once into a long array of ids. Split it by position into training and validation parts (never interleaved, so validation text is truly unseen). A training example is a window $x = \text{ids}[s : s + T]$ with targets $y = \text{ids}[s + 1 : s + T + 1]$: every position predicts the next token, so one window gives $T$ predictions.

## 4. Weight tying

The input embedding $E$ ($V \times d$) and the output layer both relate token ids to $d$-dimensional vectors. **Tying** them, logits $= hE^\top$, saves $Vd$ parameters and often trains better. The gradient of $E$ is the sum of two contributions: from the output scores, $G^\top h$, and from the rows that were looked up as inputs.

:::edge{from=L13 text="the decoder-only transformer"}
:::

## 5. Sampling

At generation time the model gives logits $z$ for the next token. **Temperature** $T$ samples from $\operatorname{softmax}(z/T)$: $T < 1$ sharpens the distribution, $T > 1$ flattens it, and $T \to 0$ becomes greedy argmax. **Top-k** keeps only the $k$ most likely tokens. **Top-p** (nucleus) keeps the smallest set of most likely tokens whose total probability is at least $p$, so the number kept adapts to how confident the model is.

::::derivation{id=d3 title="Temperature and nucleus"}
:::step
For logits $(2, 1, 0)$ at $T = 1$, the first token's probability is $e^2/(e^2 + e + 1) \approx$ [[0.665|tol=0.002]].
:::
:::step
At $T = 0.5$ the logits become $(4, 2, 0)$ and that probability rises to about [[0.867|tol=0.002]].
:::
:::step
At $T = 1$ the probabilities are about $(0.665, 0.245, 0.090)$. Top-p with $p = 0.9$ keeps [[2]] tokens.
:::
::::

:::edge{to=L15 text="Scaling laws fit this validation loss against size, data and compute."}
:::

:::edge{to=L16 text="Tokenizing and windowing billions of tokens: data pipelines."}
:::

:::edge{from=L17 text="training in reduced precision"}
:::
