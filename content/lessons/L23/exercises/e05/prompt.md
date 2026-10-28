# Is the probe finding the property?

A probe that reaches 95% may be reading the property, or memorizing word identities that happen to correlate with it. Hewitt and Liang's **control task** gives every word type a random but consistent label: a probe that does as well on the control has learned word identities, not the property. `train_probe` and `probe_accuracy` are provided.

1. `control_labels(word_ids, seed=0)`: a random 0/1 label per word type, consistent across occurrences.
2. `selectivity(A_tr, y_tr, A_te, y_te, c_tr, c_te)`: held-out accuracy on the real labels minus held-out accuracy on the control labels.

## Hints

1. Build a table from each distinct word id to a random label.
2. High selectivity means the representation encodes the property more readily than arbitrary word identities.
3. Report probe accuracy together with selectivity.
