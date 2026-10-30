# Scale: mini-batches, hashes and huge counts

Machine learning pipelines count at scale: how many mini-batches can a dataset produce, and how many bits does a hash need so that deduplicating a billion documents never confuses two of them?

## Numbers too big to hold

$\binom{10^6}{256}$ has more than a thousand digits. Python's integers can hold it, but you rarely need every digit: its logarithm, from the log-gamma function, is enough.

:::exercise{ref=e10}
:::

## Hash collisions

::::predict{id=p4 kind=numeric answer=116 tol=30}
A million distinct items are hashed to 32-bit values (about $4.3 \times 10^9$ of them), uniformly at random. About how many pairs of items collide?

:::reveal
The number of pairs is $\binom{10^6}{2} \approx 5 \times 10^{11}$, and each pair collides with probability $1/2^{32}$, so about $5 \times 10^{11} / 4.3 \times 10^9 \approx 116$ pairs collide. Expected counts of pairs simply add (linearity, M05), even though the pairs are not independent. A 32-bit hash is far too short to deduplicate a million items.
:::
::::

:::exercise{ref=e11}
:::

:::exercise{ref=e12}
:::

The widget's birthday curve is the same curve as the hash-collision curve, with 365 slots instead of $2^{32}$. Only the scale on the horizontal axis changes, by a factor of $\sqrt{2^{32}/365}$.

:::widget{name=CountingTree mode=birthday m=40}
:::
