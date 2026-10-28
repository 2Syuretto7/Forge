import sub

prose = ("It was the best of times, and it was the worst of times; the people of that age had "
         "little to do with the ones who came before, but they were happy enough with what they had. ") * 3
spam = "buy cheap watches best price watches online discount watches free shipping " * 8
table = "\n".join(f"{i} | {i * 3} | {i * 7} | #{i}" for i in range(40))
bullets = "\n".join(f"- item number {i} of the list and more" for i in range(60))


def test_signals():
    s = sub.quality_signals("The cat... #tag\n- one\nand two...")
    assert s["n_words"] == 7 and s["stop_words"] == 2
    assert abs(s["symbol_ratio"] - 2 / 7) < 1e-12
    assert abs(s["bullet_lines"] - 1 / 3) < 1e-12 and abs(s["ellipsis_lines"] - 1 / 3) < 1e-12


def test_rules():
    assert sub.passes(prose)
    assert not sub.passes(spam)
    assert not sub.passes(table)
    assert not sub.passes(bullets)
    assert not sub.passes("too short, and with the words")
