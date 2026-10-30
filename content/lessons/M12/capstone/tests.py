import numpy as np
import sub

REP = sub.report()


def test_all_recovered():
    assert len(REP) == 6
    tol = [0.01, 1e-4, 1e-3, 1e-9, 1e-3, 1e-3]
    for row, t in zip(REP, tol):
        assert row["err_qr"] < t, f"{row['name']}: QR error {row['err_qr']:.2e}"


def test_beats_baseline_when_ill_conditioned():
    for row in REP:
        if "ill conditioned" in row["name"]:
            assert row["err_normal"] > 100 * row["err_qr"], f"{row['name']}: normal {row['err_normal']:.2e}, QR {row['err_qr']:.2e}"


def test_diagnostics():
    for row in REP:
        assert row["orth"] < 1e-6, f"{row['name']}: residual not perpendicular ({row['orth']:.2e})"
    conds = {r["name"]: r["cond"] for r in REP}
    assert conds["line"] < 100
    assert min(v for k, v in conds.items() if "ill" in k) > 1e5


def test_diagnostics_on_a_bad_fit():
    ds = sub.datasets()[0]
    d = sub.diagnostics(ds["X"], ds["y"], ds["coef"] + np.array([0.0, 0.1]))
    assert d["orth"] > 0.1
