import unittest
import numpy as np
import sub


def test_exact_dedup_and_boilerplate():
    docs = ["A b", "a  B", "c\nfooter", "d\nfooter", "e"]
    assert sub.exact_dedup(docs) == [0, 2, 3, 4]
    assert sub.strip_boilerplate(docs, 2) == ["A b", "a  B", "c", "d", "e"]


def test_quality_rules():
    prose = "It was the best of times, and it was the worst of times, and that was all there was to it. " * 4
    assert sub.passes_quality(prose)
    assert not sub.passes_quality(" ".join(["buy cheap watches online now"] * 20))
    assert not sub.passes_quality("\n".join(f"{i} | {i * 7} | {i * 9}" for i in range(60)))


def test_minhash_and_near_dedup():
    doc = sub.source_docs[0]
    copy = doc.replace("the", "a", 1)
    other = sub.source_docs[5]
    sigs = [sub.minhash(doc), sub.minhash(copy), sub.minhash(other)]
    assert np.mean(sigs[0] == sigs[1]) > 0.8 and np.mean(sigs[0] == sigs[2]) < 0.3
    assert sub.near_dedup(sigs) == [0, 2]


def test_decontaminate():
    v = sub.val_docs[3]
    docs = [sub.source_docs[0], "Intro. " + v.upper(), sub.source_docs[1]]
    assert sub.decontaminate(docs, [v]) == [0, 2]


def test_pipeline_removes_the_noise():
    kept = {k: sub.kept_kinds.count(k) for k in set(sub.kinds)}
    assert kept.get("leak", 0) == 0
    assert kept.get("junk", 0) <= 0.02 * sub.kinds.count("junk")
    # Each source document and its copies should leave exactly one survivor.
    per_source = np.bincount([o for o in sub.kept_origins if o >= 0], minlength=len(sub.source_docs))
    assert np.mean(per_source == 1) >= 0.95, np.bincount(per_source)
    assert per_source.sum() <= 1.02 * len(sub.source_docs)
    assert all(sub.FOOTER not in d for d in sub.clean_docs)


def test_cleaning_helps_at_equal_compute():
    if sub.SMALL:
        raise unittest.SkipTest("the comparison needs the full training runs")
    assert sub.results["clean"]["test"] < sub.results["raw"]["test"] - 0.03, sub.results


def test_contamination_shows():
    if sub.SMALL:
        raise unittest.SkipTest("the comparison needs the full training runs")
    raw, clean = sub.results["raw"], sub.results["clean"]
    assert raw["leaked"] < raw["unleaked"] - 0.05, raw
    assert abs(clean["leaked"] - clean["unleaked"]) < abs(raw["leaked"] - raw["unleaked"]), (raw, clean)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "test loss" in text and "contamination" in text
