# Finding contamination

If benchmark text leaks into the training set, the model can memorize answers and its score stops measuring generalization (L02's test-set leakage, at web scale). GPT-3's authors flagged training documents that share any 13-word sequence with an evaluation example.

1. `words_of(doc)`: lowercased words with surrounding punctuation stripped, empty ones dropped.
2. `ngrams(words, n=13)`: the set of $n$-word tuples.
3. `build_index(eval_docs, n=13)`: the union of all evaluation documents' $n$-grams.
4. `decontaminate(train_docs, eval_docs, n=13)`: the indices of the training documents that share no $n$-gram with the evaluation set.

## Hints

1. Tuples are hashable, so a set of tuples is the index.
2. Normalizing words first catches leaks that differ only in case or punctuation.
3. A document shorter than $n$ words has no $n$-grams and is never flagged; choose $n$ to balance missed leaks against false alarms on common phrases.
