# Capstone: clean a crawl, then prove it helped

Open the Colab notebook with a **T4 GPU** runtime and work through it:

1. Write `exact_dedup` and `strip_boilerplate`.
2. Write `passes_quality` with the Gopher rules.
3. Write `minhash` over character 5-gram shingles and `near_dedup` with LSH bands and union-find.
4. Write `decontaminate` with 13-word overlaps against the validation documents.
5. Run the pipeline, then train the same model for the same number of steps on the raw and on the cleaned crawl.
6. Write a report of at least 80 words: what each step removed, the test-loss difference, and what the leaked and unleaked validation losses show.

The autograder checks each step on small cases, that no leaked document and at most 2% of the junk survive, that each source document leaves exactly one survivor, that cleaning lowers the test loss by at least **0.03 nats per byte** at equal compute, that the raw model's validation loss is inflated on the leaked documents, and the report.
