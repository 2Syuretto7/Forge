# Explain it plainly: from a crawl to training data

Explain to a new engineer what happens between a raw web crawl and the token stream a model trains on, and why each step matters.

- Write 150 to 400 words.
- Cover deduplication (including how near-duplicates are found without comparing every pair), quality filtering and decontamination.
- Give one way a careless pipeline makes a model look better than it is.

:::feynman{id=f1 prompt="Explain the steps that turn a raw web crawl into training data, including how near-duplicates are found efficiently, and one way a careless pipeline can make a model look better than it is." key_points="Exact duplicates are removed by hashing normalized documents, and repeated boilerplate lines are stripped|Near-duplicates are found with MinHash signatures, whose agreement rate estimates Jaccard similarity of shingle sets|Locality-sensitive hashing with bands makes only likely pairs candidates, avoiding comparing every pair|Quality filters use rules or a classifier trained against reference text, and a classifier can remove good text unlike its reference|Evaluation text leaking into training data inflates scores, so training data is decontaminated with n-gram overlap against evaluation sets"}
:::
