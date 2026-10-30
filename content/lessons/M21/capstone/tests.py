import sub

REP = sub.report()


def test_accuracy_and_calibration():
    assert REP["accuracy"] > 0.95, REP
    assert REP["temperature"] > 1.2, REP
    assert REP["ece_after"] < 0.015 and REP["ece_after"] < REP["ece_before"], REP


def test_note():
    words = sub.NOTE.split()
    assert len(words) >= 60
    text = sub.NOTE.lower()
    assert "phrase" in text and "temperature" in text
