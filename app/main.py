import requests
import hashlib
import json
import time
from bs4 import BeautifulSoup
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_FILE = BASE_DIR / "data" / "sites.json"
STATE_FILE = BASE_DIR / "data" / "state.json"

headers = {
    "User-Agent": "MyFeedBot/1.0 (personal use)"
}

def fetch(site):
    url = site["url"]

    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            break
        except requests.exceptions.RequestException:
            if i == 2:
                print(f"Failed: {url}")
                return None
            time.sleep(5)

    print(f"{url} -> {res.status_code}")

    if res.status_code == 404:
        print("Page not found")
        return None

    if res.status_code != 200:
        return None

    html = res.text

    if site["mode"] == "full":
        return html

    elif site["mode"] == "selector":
        soup = BeautifulSoup(html, "html.parser")
        tag = soup.select_one(site["selector"])
        return tag.text.strip() if tag else ""

    return None


def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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