import time
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

from fetch import fetch
from hash_text import hash_text
from load_json import load_json
from save_json import save_json

CONFIG_FILE = BASE_DIR / "data" / "sites.json"
STATE_FILE = BASE_DIR / "data" / "state.json"

def main():
    sites = load_json(CONFIG_FILE)
    state = load_json(STATE_FILE)

    for site in sites:
        content = fetch(site)

        if content is None:
            continue

        new_hash = hash_text(content)
        name = site["name"]

        old_hash = state.get(name)

        if old_hash and old_hash != new_hash:
            print(f"Updated: {name}")

        state[name] = new_hash

        time.sleep(10)

    save_json(STATE_FILE, state)

if __name__ == "__main__":
    main()