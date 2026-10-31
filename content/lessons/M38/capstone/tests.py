import re
import numpy as np
import sub

GRAPH = """
L01-L02 L01-L03 L01-L09 L01-M30 L02-L11 L02-L12 L02-M31 L03-L04 L03-L05 L03-L09 L03-L17
L04-L05 L04-L07 L04-L14 L05-L04 L05-L06 L05-L11 L05-L15 L05-M29 L06-L08 L06-L09 L06-M34
L07-L08 L07-L09 L07-L13 L07-L14 L07-M33 L08-L06 L08-L18 L09-L07 L09-L08 L09-L10 L09-L16
L09-L18 L09-L19 L09-M34 L10-L11 L10-L12 L10-L13 L11-L12 L11-L14 L11-L15 L11-L20 L11-M35
L12-L11 L12-L15 L13-L10 L13-L14 L13-L18 L14-L15 L15-L16 L15-L20 L16-L17 L16-L18 L16-L20
L17-L19 L17-L20 L17-M36 L18-L16 L18-L20 L19-L20 L20-M38 M01-M02 M01-M06 M01-M08 M01-M35
M02-M03 M02-M04 M02-M11 M02-M12 M03-M05 M03-M08 M03-M31 M04-L03 M04-M05 M04-M06 M04-M07
M04-M09 M05-M06 M05-M08 M05-M15 M05-M29 M06-M01 M06-M07 M06-M15 M06-M26 M06-M27 M07-L09
M07-M06 M07-M09 M08-M01 M08-M21 M08-M31 M09-M10 M09-M34 M10-L09 M10-M11 M10-M18 M11-M12
M11-M26 M12-L01 M12-M13 M12-M22 M12-M25 M13-M14 M13-M18 M13-M23 M13-M28 M13-M29 M13-M32
M14-L16 M14-M23 M14-M33 M14-M34 M15-M16 M15-M17 M15-M24 M15-M26 M16-M18 M16-M25 M16-M29
M17-M20 M17-M22 M17-M24 M18-M13 M18-M19 M18-M20 M18-M28 M19-L03 M19-L04 M19-M26 M19-M27
M20-M23 M20-M37 M21-M22 M21-M27 M22-M12 M22-M23 M22-M24 M22-M27 M22-M32 M23-M14 M23-M37
M24-M15 M24-M17 M24-M25 M24-M26 M24-M29 M24-M31 M24-M36 M25-L01 M25-L02 M25-L19 M25-M12
M25-M27 M25-M28 M25-M31 M25-M35 M26-L13 M26-M11 M26-M19 M26-M24 M26-M33 M27-L02 M27-L10
M27-L17 M27-M19 M27-M21 M27-M25 M27-M30 M27-M36 M28-L05 M28-M25 M28-M29 M28-M30 M29-L05
M29-M32 M29-M35 M29-M36 M30-L01 M30-L17 M30-M38 M31-L02 M31-M34 M32-M29 M32-M37 M33-L07
M33-M34 M33-M38 M34-L06 M34-L09 M34-M33 M34-M38 M35-L11 M35-M38 M36-L17 M36-M38 M37-M38
M38-L20
"""
EDGES = {tuple(e.split("-")) for e in GRAPH.split()}

REQUIRED = {"dpo": {"M27", "M30", "M36"}, "lora": {"M14", "M19", "M33"}, "adam": {"M16", "M24", "M29"}}
IDS = {e for pair in EDGES for e in pair}


def test_reproduction():
    assert sub.PAPER in REQUIRED
    if sub.PAPER == "dpo":
        r = sub.reproduce_dpo()
        assert r["tv"] < 0.05 and r["tv_ref"] > 0.2, r
    elif sub.PAPER == "lora":
        r = sub.reproduce_lora()
        assert r["lora_loss"] < 1.05 * r["full_loss"] and r["fraction"] < 1 / 3, r
    else:
        r = sub.reproduce_adam()
        assert r["gd_steps"] > 5 * r["adam_steps"] and r["adam_x"] == 1.0 and abs(r["amsgrad_x"] + 1) < 0.01, r


def test_lesson_map():
    lessons = set(sub.LESSONS)
    assert len(lessons) >= 6 and lessons <= IDS, lessons - IDS
    assert REQUIRED[sub.PAPER] <= lessons
    edges = [tuple(e) for e in sub.EDGES_TRAVELLED]
    assert len(set(edges)) >= 5
    for a, b in edges:
        assert (a, b) in EDGES, (a, b)
        assert a in lessons and b in lessons


def test_texts():
    assert len(sub.DERIVATION.split()) >= 250 and len(sub.REPORT.split()) >= 120
    named = set(re.findall(r"\b[ML]\d\d\b", sub.DERIVATION))
    assert len(named & set(sub.LESSONS)) >= 4
