import time
from pathlib import Path
from .fetcher import fetch
from .parser import parse
from .utils import hash_text
from .storage import load_json, save_json
from .logger import setup_logger
from page_update_monitor.config import CONFIG_FILE, STATE_FILE

logger = setup_logger()

def run_monitor():
    sites = load_json(CONFIG_FILE, [])
    state = load_json(STATE_FILE, {})
    logger.info("Start monitoring")

    for site in sites:
        html = fetch(site["url"])
        logger.info(f"Checking: {site['name']}")
        if html is None:
            continue

        content = parse(site, html)
        new_hash = hash_text(content)

        name = site["name"]
        old_hash = state.get(name)

        if old_hash and old_hash != new_hash:
            logger.info(f"Updated: {site['name']}")
            # print(f"Updated: {name}")

        state[name] = new_hash

        time.sleep(10)

    save_json(STATE_FILE, state)