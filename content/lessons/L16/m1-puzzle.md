# Puzzle: what is in a web crawl?

A raw crawl of the web is mostly not prose: navigation menus, cookie banners, product listings, machine-generated pages, the same news story syndicated to hundreds of sites, and forum posts quoting benchmark questions.

::::predict{id=p1 kind=choice answer=b}
You train two identical models with identical compute: one on a raw crawl, one on the same crawl after removing duplicates and junk, which leaves 40% of the text. Which reaches the lower loss on clean held-out text?

- The raw crawl, because it has 2.5 times as much data.
- The cleaned crawl, because every token it trains on is unique and useful.
- They are equal, because compute is equal.
- It depends only on the model size.

:::reveal
At fixed compute both models see the same number of tokens. On the raw crawl many of those tokens are repeats or junk, so the model effectively trains on less, and on text unlike the held-out set. Deduplication and filtering usually help at equal compute: Lee et al. (2022) found that models trained on deduplicated data matched or beat the originals in fewer steps and emitted memorized training text far less often. The capstone measures the effect on your own corpus.
:::
::::

::::predict{id=p2 kind=numeric answer=5e17 tol=0.1e17}
To find near-duplicates by comparing every pair of a billion documents, how many pairs would you compare?

:::reveal
$\binom{10^9}{2} = 10^9 (10^9 - 1)/2 \approx 5 \times 10^{17}$. At a million comparisons per second that is 16,000 years. MinHash compresses each document into a short signature, and locality-sensitive hashing compares only documents that collide in a bucket: the work becomes roughly linear in the corpus.
:::
::::
