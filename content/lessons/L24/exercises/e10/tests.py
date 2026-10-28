import sub

raw = sub.digest("raw corpus v1")


def chain():
    recs, inp = [], raw
    for stage, cfg, out in [("data", {"min_len": 50}, "clean"), ("pretrain", {"steps": 3000}, "base.pt"),
                            ("finetune", {"rank": 8}, "sft.pt"), ("rl", {"beta": 0.05}, "rl.pt")]:
        r = sub.make_record(stage, inp, cfg, out)
        recs.append(r)
        inp = r["output"]
    return recs


def test_records():
    r = chain()[1]
    assert r["stage"] == "pretrain" and r["config"] == sub.digest({"steps": 3000}) and r["output"] == sub.digest("base.pt")
    assert sub.check_chain(chain(), raw) is None


def test_broken_link():
    recs = chain()
    recs[2]["input"] = sub.digest("an older base.pt")
    assert sub.check_chain(recs, raw) == 2
    assert sub.check_chain(chain(), sub.digest("raw corpus v2")) == 0
