import time
from pathlib import Path

from .fetcher import fetch
from .parser import parse
from .utils import hash_text
from .storage import load_json, save_json

BASE_DIR = Path(__file__).resolve().parents[2]

CONFIG_FILE = BASE_DIR / "data" / "sites.json"
STATE_FILE = BASE_DIR / "data" / "state.json"

def run_monitor():
    sites = load_json(CONFIG_FILE, [])
    state = load_json(STATE_FILE, {})

    for site in sites:
        html = fetch(site["url"])
        if html is None:
            continue

        content = parse(site, html)
        new_hash = hash_text(content)

        name = site["name"]
        old_hash = state.get(name)

        if old_hash and old_hash != new_hash:
            print(f"Updated: {name}")

        state[name] = new_hash

        time.sleep(10)

    save_json(STATE_FILE, state)