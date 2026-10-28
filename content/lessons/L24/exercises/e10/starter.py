import hashlib
import json


def digest(obj):
    """The first 12 hex characters of the SHA-256 of obj as sorted JSON."""
    raise NotImplementedError


def make_record(stage, input_digest, config, output):
    """A manifest record for one stage: its name, the digest of what it read, and the digests of
    its configuration and of what it wrote."""
    raise NotImplementedError


def check_chain(records, first_input):
    """Index of the first record whose input is not the output of the record before it (or
    first_input for the first record), or None if the chain is intact."""
    raise NotImplementedError
