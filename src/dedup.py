import json
import os

from . import config


def load_seen():
    # load the set of accession numbers we already proccessed
    if not os.path.exists(config.SEEN_FILE):
        return set()
    with open(config.SEEN_FILE) as f:
        return set(json.load(f))


def save_seen(seen):
    # save the set back to disk so restarts dont re-download everything
    os.makedirs(config.DATA_DIR, exist_ok=True)
    with open(config.SEEN_FILE, "w") as f:
        json.dump(sorted(seen), f)
