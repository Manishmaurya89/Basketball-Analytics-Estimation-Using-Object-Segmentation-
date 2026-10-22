"""Pickle cache for slow steps (detection, tracking, team assignment) so reruns are fast."""

import os
import pickle


def save_stub(stub_path, obj):
    if stub_path is None:
        return
    os.makedirs(os.path.dirname(os.path.abspath(stub_path)), exist_ok=True)
    with open(stub_path, 'wb') as f:
        pickle.dump(obj, f)


def read_stub(read_from_stub, stub_path):
    """Return the cached object, or None if caching is off or nothing is cached yet."""
    if read_from_stub and stub_path is not None and os.path.exists(stub_path):
        with open(stub_path, 'rb') as f:
            return pickle.load(f)
    return None
