import hashlib
import json


def digest(obj):
    """The first 12 hex characters of the SHA-256 of obj as sorted JSON."""
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def make_record(stage, input_digest, config, output):
    """A manifest record for one stage: its name, the digest of what it read, and the digests of
    its configuration and of what it wrote."""
    return {"stage": stage, "input": input_digest, "config": digest(config), "output": digest(output)}


def check_chain(records, first_input):
    """Index of the first record whose input is not the output of the record before it (or
    first_input for the first record), or None if the chain is intact."""
    expected = first_input
    for i, r in enumerate(records):
        if r["input"] != expected:
            return i
        expected = r["output"]
    return None
