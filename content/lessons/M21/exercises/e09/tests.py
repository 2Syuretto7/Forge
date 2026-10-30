import sub


def test_hospital_and_screening():
    r = sub.rates(tp=180, fn=20, fp=40, tn=760)
    assert abs(r["sensitivity"] - 0.9) < 1e-12 and abs(r["specificity"] - 0.95) < 1e-12
    assert abs(r["ppv"] - 180 / 220) < 1e-12 and abs(r["npv"] - 760 / 780) < 1e-12
    assert abs(sub.ppv_at(0.2, 0.9, 0.95) - r["ppv"]) < 1e-12
    assert sub.ppv_at(0.001, 0.9, 0.95) < 0.02
