# Derivation: duplicates, quality, mixtures and leaks

## 1. Why data quality changes scaling

In L15's law $L = E + A N^{-\alpha} + B D^{-\beta}$, $D$ counts useful tokens. If a fraction $f$ of training tokens is junk, a model trained on $D$ tokens learns as if from about $(1 - f) D$, and the data term grows by $(1-f)^{-\beta}$; duplicated text is worth less than fresh text (L15's repeated-data formula). Filtering also changes what the model learns to predict: training on text unlike the evaluation distribution moves the whole curve, not just the effective $D$.

::::derivation{id=d1 title="The cost of junk"}
:::step
With $\beta = 0.28$ and a quarter of the tokens wasted, the data term grows by $0.75^{-0.28} \approx$ [[1.084|tol=0.001]].
:::
:::step
To recover that loss with more raw data, you need $1/(1 - f) =$ [[1.333|tol=0.001]] times as many raw tokens, and as much more compute.
:::
::::

:::edge{to=L15 text="data quality shifts the scaling curve"}
:::

## 2. Exact duplicates

Normalize each document (case, whitespace), hash it, and keep the first document with each hash. With a $b$-bit hash and $n$ documents, the chance that two different documents collide is about $n^2 / 2^{b+1}$ (the birthday bound), so use a cryptographic hash such as SHA-1 (160 bits) rather than a 32- or 64-bit one. The same trick removes **boilerplate**: lines that occur on many different pages are navigation and footers, not content.

::::derivation{id=d2 title="The birthday bound"}
:::step
With a 64-bit hash and $n = 10^9$ documents, the probability of at least one false collision is about $n^2 / 2^{65} \approx$ [[0.0271|tol=0.0005]].
:::
:::step
With 160 bits it is about $10^{18}/2^{161}$, around $10^{-30}$: never.
:::
::::

## 3. Near duplicates: Jaccard similarity and MinHash

Represent a document by its set of **shingles**, the overlapping character (or word) $k$-grams. Two documents are near-duplicates when the **Jaccard similarity** $J(A, B) = |A \cap B|/|A \cup B|$ of their shingle sets is high.

**MinHash.** Take a random hash function $h$ (in effect, a random ordering of all possible shingles) and record the smallest hash in each set. The smallest element of $A \cup B$ is equally likely to be any of its members, and the two minima agree exactly when that element lies in $A \cap B$. So
$$
\Pr\bigl[\min h(A) = \min h(B)\bigr] = \frac{|A \cap B|}{|A \cup B|} = J(A, B).
$$
With $k$ independent hash functions the fraction of agreeing minima is an unbiased estimate of $J$ with standard deviation $\sqrt{J(1-J)/k}$. Each document shrinks to a signature of $k$ integers, whatever its length.

::::derivation{id=d3 title="MinHash accuracy"}
:::step
For $J = 0.8$ and $k = 128$, the standard deviation of the estimate is $\sqrt{0.8 \cdot 0.2/128} \approx$ [[0.0354|tol=0.0005]].
:::
:::step
To halve it you need [[4]] times as many hash functions.
:::
::::

## 4. Locality-sensitive hashing: comparing only likely pairs

Cut each signature into $b$ bands of $r$ rows and hash every band into a bucket. Two documents with similarity $s$ match on one given band with probability $s^r$ (all $r$ rows must agree), so they fail to share any band with probability $(1 - s^r)^b$, and become **candidates** with probability
$$
P(s) = 1 - (1 - s^r)^b.
$$
This is an S-shaped curve, steepest near $s^* \approx (1/b)^{1/r}$. Only candidates are compared, so the work is roughly linear in the corpus. Choose $b$ and $r$ so that the curve rises around your similarity cutoff: more rows per band push it right and make it steeper; more bands push it left.

::::derivation{id=d4 title="An S-curve"}
:::step
With $b = 16$ bands of $r = 8$ rows, a pair with $s = 0.8$ becomes a candidate with probability $1 - (1 - 0.8^8)^{16} \approx$ [[0.947|tol=0.001]].
:::
:::step
A pair with $s = 0.5$ does so with probability about [[0.0607|tol=0.0005]].
:::
:::step
The threshold $(1/16)^{1/8}$ is about [[0.7071|tol=0.0005]].
:::
::::

Move the threshold around with the widget, and see how many hashes you need for a sharp cut.

:::widget{name=LshCurve}
:::

## 5. Quality filtering

**Rules.** The Gopher pipeline (Rae et al., 2021) removed documents outside 50 to 100,000 words, with a mean word length outside 3 to 10 characters, with too many symbols, bullets or trailing ellipses, with fewer than 80% of words containing a letter, or without at least two common English function words. Each rule targets a kind of junk: lists, tables, code dumps, keyword spam.

**Classifiers.** GPT-3's pipeline trained a logistic-regression classifier on hashed word features to distinguish curated reference text from raw crawl, and kept crawl documents stochastically, favoring those that scored like the reference. A classifier is only as good as its reference set: it also removes good text that looks unlike the reference, such as other dialects and genres.

## 6. Mixtures

A training set mixes domains of very different sizes. Sampling with weights $p_j$ for a budget of $T$ tokens repeats domain $j$ for $p_j T / \text{size}_j$ epochs, so small high-quality domains are often upsampled, and multilingual models flatten the weights with a temperature, $p_j \propto \text{size}_j^{1/\tau}$.

Suppose domain $j$'s excess loss after $p_j T$ tokens is $c_j (p_j T)^{-\beta}$ and we minimize the total. A Lagrange multiplier for $\sum_j p_j = 1$ gives $\beta c_j p_j^{-\beta - 1} = \lambda$ for every $j$, so
$$
p_j \propto c_j^{1/(1 + \beta)}:
$$
domains with more left to learn get more weight, but less than proportionally.

::::derivation{id=d5 title="Optimal weights"}
:::step
With $c = (4, 1)$ and $\beta = 1$, the weights are proportional to $(4^{1/2}, 1)$, so the first domain gets $p_1 =$ [[0.667|tol=0.001]].
:::
:::step
A domain of 20 billion tokens with weight 0.1 in a run of a trillion tokens is repeated for [[5]] epochs.
:::
::::

## 7. Contamination

If evaluation text appears in the training data, a model can reproduce the answers it memorized, and the score measures memory instead of skill. GPT-3's authors flagged training documents sharing any 13-word sequence with an evaluation example and reported scores on the clean subset separately. Contamination does more than shift a number: a model that memorizes more can look better than one that generalizes better, reversing the decision the evaluation was for (exercise 11).

:::edge{from=L06 text="test-set leakage, now at web scale"}
:::

## 8. Pipelines that can stop and resume

Data at scale is read as a stream of **shards**. A loader should give each example once per epoch in a shuffled order, run on many workers, and after a crash resume **exactly** where it stopped: otherwise a resumed run sees some data twice and some never, and its results cannot be reproduced. The robust design derives every random order from the seed and the epoch (and the shard), so the loader's whole state is a few integers. Anything with hidden state, a shuffle buffer or a generator, must be saved in the checkpoint along with the model.

:::edge{from=L14 text="tokenizing and windowing a corpus"}
:::

:::edge{to=L19 text="The pretraining run reads its data through a resumable pipeline."}
:::
