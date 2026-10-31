import sub


def test_plan_is_valid_and_fits():
    p = sub.PLAN
    assert p["tp"] * p["pp"] * p["dp"] == sub.N_GPUS
    assert p["tp"] <= sub.NODE_SIZE and sub.MODEL["heads"] % p["tp"] == 0 and sub.MODEL["layers"] % p["pp"] == 0
    assert sub.GLOBAL_SEQS % (p["dp"] * p["micro"]) == 0
    assert sub.plan_bytes <= 0.9 * sub.GPU_BYTES, sub.plan_bytes
    assert sub.bubble < 0.1, sub.bubble


def test_ring_collectives():
    assert len(sub.ring_errors) == sub.WORLD and max(sub.ring_errors) < 1e-9, sub.ring_errors


def test_data_parallel_matches_one_process():
    assert sub.ddp_error < 1e-12, sub.ddp_error


def test_zero1_matches_adam_and_shards_state():
    assert sub.zero_error < 1e-10, sub.zero_error
    assert all(s <= 2 * (sub.n_params // sub.WORLD + 1) for s in sub.zero_state), sub.zero_state


def test_tensor_parallel_mlp():
    assert max(sub.tp_errors) < 1e-10, sub.tp_errors


def test_checkpointing_saves_memory():
    assert sub.ckpt_bytes < 0.25 * sub.plain_bytes, (sub.ckpt_bytes, sub.plain_bytes)


def test_report():
    text = sub.REPORT.lower()
    assert len(text.split()) >= 80
    assert "zero" in text and "gb" in text
